import psycopg2
from psycopg2 import pool
from src.config.settings import settings
from src.utils.common import setup_logger

logger = setup_logger(__name__)


class PostgresDB:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                logger.info(
                    f"Connecting to Postgres at {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT} as {settings.POSTGRES_USER}"
                )
                cls._pool = pool.ThreadedConnectionPool(
                    1,
                    20,
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD,
                    host=settings.POSTGRES_HOST,
                    port=settings.POSTGRES_PORT,
                    database=settings.POSTGRES_DB,
                )
                logger.info("PostgreSQL connection pool created successfully")
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f"Error while connecting to PostgreSQL: {error}")
                raise error
        return cls._pool

    @classmethod
    def get_connection(cls):
        _pool = cls.get_pool()
        if _pool is None:
            raise Exception("Failed to create connection pool")
        return _pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.get_pool().putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls._pool:
            cls._pool.closeall()
            logger.info("PostgreSQL connection pool is closed")
