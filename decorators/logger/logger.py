"""
This module provides a `log_execution` decorator to log the execution details 
of functions, both synchronous and asynchronous. It logs the start time, 
execution time, arguments, keyword arguments, and the return value of the 
decorated function.

The `log_execution` decorator can be applied to both regular (synchronous) 
and coroutine (asynchronous) functions. For asynchronous functions, it 
awaits the result and logs the execution time once the coroutine is complete.
"""

import asyncio
import functools
import time
import logging
from typing import Callable, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def log_execution(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    
    """
    A decorator to log the execution details of a function, including 
    its start time, execution time, arguments, and return value. It handles 
    both synchronous and asynchronous functions.

    Args:
        func (Callable[..., Any]): The function to be decorated.

    Returns:
        Callable[..., Any]: The decorated function with logging functionality.
    """
    
    @functools.wraps(func)
    def sync_wrapper(
        *args: Any, 
        **kwargs: Any,
    ) -> Any:
        
        """
        A wrapper for synchronous functions that logs execution details 
        and calculates the execution time.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            Any: The result of the decorated function.
        """
        
        start_time = time.perf_counter()
        logger.info(
            f'Executing {func.__name__} with args: {args}, kwargs: {kwargs}'
        )

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        logger.info(
            f'Finished {func.__name__} in {end_time - start_time:.4f} seconds, returned: {result}'
        )
        return result

    @functools.wraps(func)
    async def async_wrapper(
        *args: Any, 
        **kwargs: Any,
    ) -> Any:
        
        """
        A wrapper for asynchronous functions that logs execution details 
        and calculates the execution time after awaiting the result.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            Any: The result of the decorated asynchronous function.
        """
        
        start_time = time.perf_counter()
        logger.info(
            f'Executing async {func.__name__} with args: {args}, kwargs: {kwargs}'
        )

        result = await func(*args, **kwargs)

        end_time = time.perf_counter()
        logger.info(
            f'Finished async {func.__name__} in {end_time - start_time:.4f} seconds, returned: {result}'
        )
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
