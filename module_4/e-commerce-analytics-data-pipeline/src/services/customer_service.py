from ..database.postgres import PostgresDB
from ..utils.common import setup_logger

logger = setup_logger(__name__)


class CustomerService:
    def create_customer(self, name: str, email: str):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING customer_id",
                    (name, email),
                )
                customer_id = cur.fetchone()[0]
                conn.commit()
                return customer_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating customer: {e}")
            raise
        finally:
            PostgresDB.return_connection(conn)

    def get_customer(self, customer_id: int):
        conn = PostgresDB.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT customer_id, name, email, created_at FROM customers WHERE customer_id = %s",
                    (customer_id,),
                )
                row = cur.fetchone()
                if row:
                    return {
                        "customer_id": row[0],
                        "name": row[1],
                        "email": row[2],
                        "created_at": str(row[3]),
                    }
                return None
        except Exception as e:
            logger.error(f"Error getting customer: {e}")
            return None
        finally:
            PostgresDB.return_connection(conn)
