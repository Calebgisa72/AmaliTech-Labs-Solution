import redis
from ..config.settings import settings
from ..utils.common import setup_logger

logger = setup_logger(__name__)


def get_redis_client():
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=int(settings.REDIS_PORT),
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        # Test connection
        r.ping()
        return r
    except redis.ConnectionError as e:
        logger.error(f"Error connecting to Redis: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected Redis error: {e}")
        return None
