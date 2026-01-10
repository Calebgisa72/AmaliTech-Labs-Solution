import json
from src.database.postgres import PostgresDB
from src.database.redis_client import get_redis_client
from src.utils.common import setup_logger

logger = setup_logger(__name__)


class ProductService:
    def add_product(
        self, name: str, category: str, price: float, stock: int, metadata: dict
    ):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO products (name, category, price, stock_quantity, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING product_id;
                    """,
                    (name, category, price, stock, json.dumps(metadata)),
                )
                product_id = cur.fetchone()[0]
                conn.commit()
                # Optionally cache the new product immediately
                return product_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error adding product: {e}")
            raise
        finally:
            PostgresDB.return_connection(conn)

    def get_product(self, product_id: int):
        # 1. Check Redis Cache
        redis_client = get_redis_client()
        cache_key = f"product:{product_id}"

        if redis_client:
            cached_product = redis_client.get(cache_key)
            if cached_product:
                logger.info(f"Cache hit for product {product_id}")
                return json.loads(cached_product)

        # 2. Fetch from Postgres
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT product_id, name, category, price, stock_quantity, metadata FROM products WHERE product_id = %s",
                    (product_id,),
                )
                row = cur.fetchone()
                if row:
                    product = {
                        "product_id": row[0],
                        "name": row[1],
                        "category": row[2],
                        "price": float(row[3]),
                        "stock_quantity": row[4],
                        "metadata": (
                            row[5] if isinstance(row[5], dict) else json.loads(row[5])
                        ),
                    }

                    # 3. Cache in Redis (TTL 1 hour)
                    if redis_client:
                        redis_client.set(cache_key, json.dumps(product), ex=3600)

                    return product
                return None
        except Exception as e:
            logger.error(f"Error fetching product: {e}")
            return None
        finally:
            PostgresDB.return_connection(conn)

    def update_stock(self, product_id: int, quantity: int):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s RETURNING stock_quantity",
                    (quantity, product_id),
                )
                new_stock = cur.fetchone()
                conn.commit()

                # Invalidate cache since stock changed
                redis_client = get_redis_client()
                if redis_client:
                    redis_client.delete(f"product:{product_id}")

                return new_stock[0] if new_stock else None
        except Exception as e:
            conn.rollback()
            logger.error(f"Error updating stock: {e}")
            raise
        finally:
            PostgresDB.return_connection(conn)

    def get_all_products(self):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT product_id, name, category, price, stock_quantity, metadata FROM products"
                )
                rows = cur.fetchall()
                products = []
                for row in rows:
                    products.append(
                        {
                            "product_id": row[0],
                            "name": row[1],
                            "category": row[2],
                            "price": float(row[3]),
                            "stock_quantity": row[4],
                            "metadata": (
                                row[5]
                                if isinstance(row[5], dict)
                                else json.loads(row[5])
                            ),
                        }
                    )
                return products
        except Exception as e:
            logger.error(f"Error fetching all products: {e}")
            return []
        finally:
            PostgresDB.return_connection(conn)
