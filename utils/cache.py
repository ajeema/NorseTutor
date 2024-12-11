import redis
from config import Config

cache = redis.from_url(Config.REDIS_URL)

def cache_set(key, value, ex=3600):
    cache.set(key, value, ex=ex)

def cache_get(key):
    return cache.get(key)
