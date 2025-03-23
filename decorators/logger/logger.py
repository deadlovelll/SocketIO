import asyncio
import functools
import time
import logging

from typing import Callable, Any

logging.basicConfig (
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def log_execution (
    func: Callable[..., Any],
) -> Callable[..., Any]:
    
    @functools.wraps(func)
    def sync_wrapper (
        *args, 
        **kwargs,
    ) -> Any:
        
        start_time = time.perf_counter()
        logger.info (
            f'Executing {func.__name__} with args: {args}, kwargs: {kwargs}'
        )
        
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        logger.info (
            f'Finished {func.__name__} in {end_time - start_time:.4f} seconds, returned: {result}'
        )
        return result
    
    @functools.wraps(func)
    async def async_wrapper (
        *args, 
        **kwargs,
    ) -> Any:
        
        start_time = time.perf_counter()
        logger.info (
            f'Executing async {func.__name__} with args: {args}, kwargs: {kwargs}'
        )
        
        result = await func(*args, **kwargs)
        
        end_time = time.perf_counter()
        logger.info (
            f'Finished async {func.__name__} in {end_time - start_time:.4f} seconds, returned: {result}'
        )
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

