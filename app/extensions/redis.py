# app/extensions/redis.py
from flask import current_app
from redis import Redis

redis = Redis()

def get_redis():
    """Get Redis connection."""
    return redis.from_url(current_app.config['REDIS_URL'])

class RedisService:
    @staticmethod
    def set_key(key, value, expiry=None):
        client = get_redis()
        client.set(key, value, ex=expiry)

    @staticmethod
    def get_key(key):
        client = get_redis()
        return client.get(key)

    @staticmethod
    def delete_key(key):
        client = get_redis()
        client.delete(key)

# Test connection
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("Connected to Redis successfully!")
except redis.ConnectionError:
    print("Redis connection failed")
