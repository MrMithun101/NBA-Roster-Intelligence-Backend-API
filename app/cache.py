"""
Redis cache-aside helper. If Redis is unavailable, get_json returns None and
set_json is a no-op so the API continues to work without caching.
"""

import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_redis = None


def _get_client():
    """Lazy Redis connection. Returns None if Redis is down."""
    global _redis
    if _redis is not None:
        return _redis
    try:
        import redis
        _redis = redis.from_url(REDIS_URL, decode_responses=True)
        _redis.ping()
        return _redis
    except Exception:
        _redis = None
        return None


def get_json(key: str) -> Any | None:
    """
    Get a JSON value from Redis. Returns None on cache miss or any error
    (e.g. Redis down), so callers can fall back to DB.
    """
    client = _get_client()
    if not client:
        return None
    try:
        raw = client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def delete_keys_by_prefix(prefix: str) -> int:
    """
    Delete all Redis keys matching the prefix. Uses SCAN to avoid blocking.
    Returns the number of keys deleted. Safe no-op if Redis is down.
    """
    client = _get_client()
    if not client:
        return 0
    try:
        count = 0
        cursor = 0
        while True:
            cursor, keys = client.scan(cursor=cursor, match=f"{prefix}*", count=100)
            for k in keys:
                client.delete(k)
                count += 1
            if cursor == 0:
                break
        return count
    except Exception:
        return 0


def set_json(key: str, value: Any, ttl_seconds: int) -> bool:
    """
    Set a JSON value in Redis with TTL. Returns True on success, False on
    error (e.g. Redis down). No-op on failure so API still works.
    """
    client = _get_client()
    if not client:
        return False
    try:
        client.setex(key, ttl_seconds, json.dumps(value, default=str))
        return True
    except Exception:
        return False
