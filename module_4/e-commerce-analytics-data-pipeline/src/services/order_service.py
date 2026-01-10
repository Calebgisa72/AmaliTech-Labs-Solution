from src.database.postgres import PostgresDB
from src.database.mongo_client import get_mongo_db
from src.utils.common import setup_logger

logger = setup_logger(__name__)


class OrderService:
    def create_order(self, customer_id: int, cart_items: list):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                # Calculate total amount
                total_amount = sum(
                    item["quantity"] * item["price"] for item in cart_items
                )

                # Create Order Record
                cur.execute(
                    "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s) RETURNING order_id",
                    (customer_id, total_amount),
                )
                order_id = cur.fetchone()[0]

                for item in cart_items:
                    pid = item["product_id"]
                    qty = item["quantity"]
                    price = item["price"]

                    # Update Stock with check
                    cur.execute(
                        "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s AND stock_quantity >= %s RETURNING product_id",
                        (qty, pid, qty),
                    )

                    if cur.fetchone() is None:
                        raise ValueError(f"Insufficient stock for product_id {pid}")

                    # Create Order Item
                    cur.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                        (order_id, pid, qty, price),
                    )

                conn.commit()
                return order_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Order transaction failed: {e}")
            raise e
        finally:
            PostgresDB.return_connection(conn)

    def get_order_history(self, customer_id: int):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                # Use JSON aggregation to get items nested within the order
                query = """
                    SELECT o.order_id, o.total_amount, o.order_date,
                           json_agg(json_build_object('product_id', oi.product_id, 'quantity', oi.quantity, 'unit_price', oi.unit_price))
                    FROM orders o
                    JOIN order_items oi ON o.order_id = oi.order_id
                    WHERE o.customer_id = %s
                    GROUP BY o.order_id
                    ORDER BY o.order_date DESC;
                """
                cur.execute(query, (customer_id,))
                rows = cur.fetchall()

                history = []
                for row in rows:
                    history.append(
                        {
                            "order_id": row[0],
                            "total_amount": float(row[1]),
                            "order_date": str(row[2]),
                            "items": row[3],
                        }
                    )
                return history
        except Exception as e:
            logger.error(f"Error fetching order history: {e}")
            return []
        finally:
            PostgresDB.return_connection(conn)

    def add_to_cart(self, session_id: str, item: dict):
        """
        Adds an item to the user's shopping cart in MongoDB.
        item: dict with 'product_id', 'quantity', 'price'
        """
        db = get_mongo_db()
        if db is not None:
            try:
                db.carts.update_one(
                    {"session_id": session_id}, {"$push": {"items": item}}, upsert=True
                )
                logger.info(f"Item added to cart for session {session_id}")
            except Exception as e:
                logger.error(f"Error adding to cart: {e}")

    def get_cart(self, session_id: str):
        """
        Retrieves the user's shopping cart from MongoDB.
        """
        db = get_mongo_db()
        if db is not None:
            try:
                cart = db.carts.find_one({"session_id": session_id})
                return cart.get("items", []) if cart else []
            except Exception as e:
                logger.error(f"Error fetching cart: {e}")
                return []
        return []
