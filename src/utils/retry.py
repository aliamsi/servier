import time
import logging
from functools import wraps
from typing import Callable, Any

def retry_on_error(
    max_retries: int = 3,
    retry_delay: int = 1,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Decorator for retrying operations that may fail"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        logging.error(f"Failed after {max_retries} attempts: {str(e)}")
                        raise
                    logging.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. Retrying..."
                    )
                    time.sleep(retry_delay)
            return None
        return wrapper
    return decorator