"""
Performance optimization utilities.
"""

import time
from functools import wraps
from typing import Callable, Any

from app.utils.logging import logger


def time_operation(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
    
    Returns:
        Wrapped function
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        logger.debug(f"{func.__name__} took {duration:.2f}s")
        return result
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logger.debug(f"{func.__name__} took {duration:.2f}s")
        return result
    
    # Return appropriate wrapper
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator to retry function on failure.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            import time as time_module
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                        time_module.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            raise last_exception
        
        # Return appropriate wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Import asyncio for retry decorator
import asyncio
