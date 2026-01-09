import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "ecommerce_sessions")


settings = Settings()
