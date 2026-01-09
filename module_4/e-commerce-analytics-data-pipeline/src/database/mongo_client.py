from pymongo import MongoClient
from src.config.settings import settings


def get_mongo_client():
    try:
        client = MongoClient(settings.MONGO_URI)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def get_mongo_db():
    client = get_mongo_client()
    if client:
        return client[settings.MONGO_DB]
    return None
