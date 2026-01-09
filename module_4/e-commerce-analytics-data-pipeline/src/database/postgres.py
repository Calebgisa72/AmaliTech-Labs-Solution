import psycopg2
from psycopg2 import pool
from src.config.settings import settings


class PostgresDB:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = psycopg2.pool.SimpleConnectionPool(
                    1,
                    20,
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD,
                    host=settings.POSTGRES_HOST,
                    port=settings.POSTGRES_PORT,
                    database=settings.POSTGRES_DB,
                )
                print("PostgreSQL connection pool created successfully")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while connecting to PostgreSQL", error)
        return cls._pool

    @classmethod
    def get_connection(cls):
        return cls.get_pool().getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.get_pool().putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls._pool:
            cls._pool.closeall()
            print("PostgreSQL connection pool is closed")
