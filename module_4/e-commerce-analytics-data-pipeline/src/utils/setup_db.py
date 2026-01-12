from src.database.postgres import PostgresDB
from pathlib import Path
from src.utils.common import setup_logger

logger = setup_logger(__name__)


def init_db():
    logger.info("Initializing Database...")
    try:
        conn = PostgresDB.get_connection()
        cur = conn.cursor()

        schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
        logger.info(f"Reading schema from {schema_path}")

        if not schema_path.exists():
            logger.error(f"Schema file not found at {schema_path}")
            return

        schema_sql = schema_path.read_text()

        cur.execute(schema_sql)
        conn.commit()
        logger.info("Database schema created successfully.")
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        conn.rollback()
    finally:
        cur.close()
        PostgresDB.return_connection(conn)


if __name__ == "__main__":
    init_db()
