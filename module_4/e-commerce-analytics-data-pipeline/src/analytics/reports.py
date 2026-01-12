from src.database.postgres import PostgresDB
from src.database.redis_client import get_redis_client
import json
from src.utils.common import setup_logger

logger = setup_logger(__name__)


class AnalyticsReports:
    def get_top_selling_products(self, limit=10):
        """
        Get top selling products, cached in Redis.
        """
        redis_client = get_redis_client()
        cache_key = f"top_selling_products:{limit}"

        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    logger.info("Cache hit for top selling products")
                    return json.loads(cached)
            except Exception as e:
                logger.error(f"Redis cache error: {e}")

        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                query = """
                SELECT p.name, SUM(oi.quantity) as total_sold
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                GROUP BY p.product_id, p.name
                ORDER BY total_sold DESC
                LIMIT %s
                """
                cur.execute(query, (limit,))
                rows = cur.fetchall()
                result = [
                    {"product": row[0], "total_sold": int(row[1])} for row in rows
                ]

                if redis_client:
                    try:
                        redis_client.set(cache_key, json.dumps(result), ex=300)
                    except Exception as e:
                        logger.error(f"Redis set error: {e}")

                return result
        except Exception as e:
            logger.error(f"Error getting top products: {e}")
            return []
        finally:
            PostgresDB.return_connection(conn)

    def get_products_ranked_by_category(self):
        """
        Rank products by sales volume within each category using RANK() window function.
        """
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                query = """
                SELECT p.category, p.name, SUM(oi.quantity) as total_sold,
                       RANK() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity) DESC) as rank
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                GROUP BY p.category, p.product_id, p.name
                ORDER BY p.category, rank
                """
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    {
                        "category": r[0],
                        "product": r[1],
                        "sold": int(r[2]),
                        "rank": int(r[3]),
                    }
                    for r in rows
                ]
        except Exception as e:
            logger.error(f"Error getting ranked products: {e}")
            return []
        finally:
            PostgresDB.return_connection(conn)

    def get_customer_total_revenue(self):
        """
        Calculate total revenue per customer using CTE.
        """
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                query = """
                WITH CustomerRevenue AS (
                    SELECT customer_id, SUM(total_amount) as total_revenue
                    FROM orders
                    GROUP BY customer_id
                )
                SELECT c.name, cr.total_revenue
                FROM CustomerRevenue cr
                JOIN customers c ON cr.customer_id = c.customer_id
                ORDER BY cr.total_revenue DESC
                """
                cur.execute(query)
                rows = cur.fetchall()
                return [{"customer": r[0], "total_revenue": float(r[1])} for r in rows]
        except Exception as e:
            logger.error(f"Error calculating LTV: {e}")
            return []
        finally:
            PostgresDB.return_connection(conn)
