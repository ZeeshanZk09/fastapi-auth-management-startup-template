import redis.asyncio as redis
from app.config import settings

def get_redis_client():
    return redis.from_url(settings.REDIS_URL, decode_responses=True)

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
