import redis
from src.config.settings import settings


def get_redis_client():
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
        )
        return r
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None
