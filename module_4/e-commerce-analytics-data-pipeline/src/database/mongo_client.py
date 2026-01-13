from pymongo import MongoClient
from ..config.settings import settings
from ..utils.common import setup_logger

logger = setup_logger(__name__)


def get_mongo_client():
    try:
        client = MongoClient(settings.MONGO_URI)
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None


def get_mongo_db():
    client = get_mongo_client()
    if client:
        return client[settings.MONGO_DB]
    return None
