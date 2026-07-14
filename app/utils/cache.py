"""Cache utilities for reducing API calls."""

import hashlib
import json
from typing import Any, Callable, Optional
from datetime import datetime, timedelta
from functools import wraps

from app.utils.logging import logger


class SimpleCache:
    """Simple in-memory cache for function results."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time to live for cache entries
        """
        self.cache: dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def _get_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """
        Generate cache key from function and arguments.
        
        Args:
            func_name: Function name
            args: Function arguments
            kwargs: Function keyword arguments
        
        Returns:
            Cache key
        """
        key_data = {
            "func": func_name,
            "args": str(args),
            "kwargs": str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        
        if datetime.utcnow() - timestamp > self.ttl:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = (value, datetime.utcnow())
    
    def clear(self) -> None:
        """
        Clear all cache entries.
        """
        self.cache.clear()


# Global cache instance
_cache = SimpleCache(ttl_seconds=3600)


def cached(ttl_seconds: int = 3600) -> Callable:
    """
    Decorator to cache function results.
    
    Args:
        ttl_seconds: Time to live for cache entries
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        cache = SimpleCache(ttl_seconds=ttl_seconds)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            key = cache._get_key(func.__name__, args, kwargs)
            
            # Check cache
            cached_value = cache.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(key, result)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            key = cache._get_key(func.__name__, args, kwargs)
            
            # Check cache
            cached_value = cache.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(key, result)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        # Return appropriate wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
