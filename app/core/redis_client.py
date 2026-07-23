"""Redis cache helper."""

import contextlib
import json
from json import JSONDecodeError

import redis
from loguru import logger
from redis.exceptions import RedisError


class RedisCache:
    """Wrapper around Redis cache operations."""

    def __init__(self):
        self.client = None
        self._connect()

    def _connect(self):
        """Connect to Redis."""
        try:
            self.client = redis.Redis(
                host="redis", port=6379, decode_responses=True, socket_connect_timeout=3
            )
            self.client.ping()
            logger.info("Redis connection established")
        except (RedisError, ConnectionError, TimeoutError) as e:
            logger.warning(f"Unable to connect to Redis: {e}")
            self.client = None

    def get(self, key: str):
        """Return cached data for the given key."""
        if not self.client:
            return None
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)  # type: ignore
            return None
        except (RedisError, JSONDecodeError) as e:
            logger.error(f"Failed to read from Redis: {e}")
            return None

    def set(self, key: str, value, expire: int = 60):
        """Store data in the cache."""
        if not self.client:
            return
        try:
            self.client.setex(key, expire, json.dumps(value))
        except RedisError as e:
            logger.error(f"Failed to write to Redis: {e}")

    def delete(self, key: str):
        """Remove a key from the cache."""
        if self.client:
            with contextlib.suppress(RedisError):
                self.client.delete(key)


# Shared cache instance used throughout the application.
cache = RedisCache()
