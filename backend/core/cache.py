from django.core.cache import cache
from django.conf import settings
import hashlib
import json


def generate_cache_key(prefix, *args, **kwargs):
    """
    Generate a unique cache key based on prefix and parameters
    """
    key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"{prefix}:{key_hash}"


def get_cached_data(key):
    """
    Get data from cache
    """
    return cache.get(key)


def set_cached_data(key, data, timeout=None):
    """
    Set data in cache with optional timeout
    """
    if timeout is None:
        timeout = settings.CACHES['default']['TIMEOUT']
    cache.set(key, data, timeout)


def delete_cached_data(key):
    """
    Delete data from cache
    """
    cache.delete(key)


def invalidate_task_cache(task_id=None, user_id=None):
    """
    Invalidate task-related cache entries
    """
    patterns = [
        'task_list:*',
        'user_tasks:*',
        'task_detail:*',
    ]
    
    if task_id:
        cache.delete(f'task_detail:{task_id}')
    
    if user_id:
        cache.delete(f'user_tasks:{user_id}')
    
    # Invalidate list caches
    cache.delete_pattern('task_list:*')


def invalidate_event_cache():
    """
    Invalidate event-related cache entries
    """
    cache.delete_pattern('event_list:*')


class CacheManager:
    """
    Context manager for cache operations
    """
    def __init__(self, key, timeout=None):
        self.key = key
        self.timeout = timeout
        self.data = None
    
    def __enter__(self):
        self.data = get_cached_data(self.key)
        return self.data
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.data is not None:
            set_cached_data(self.key, self.data, self.timeout)
