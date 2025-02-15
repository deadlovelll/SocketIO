from typing import Callable
import functools

from decorators.cache_decorator.redis_caching.redis_caching import RedisCaching
from decorators.cache_decorator.memoize_caching.memoize_caching import MemoizeCaching
from decorators.cache_decorator.lru_caching.lru_caching import LRUCaching

class CacheDecorator:
    
    def __init__ (
        self,
    ) -> None:

        self.redis_caching = RedisCaching()
        self.memoize_caching = MemoizeCaching()
        self.lru_caching = LRUCaching()
        
    def redis_cache (
        self, 
        duration: int
    ):
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.redis_caching.cache (
                    func, 
                    duration, 
                    *args, 
                    **kwargs
                )
            return wrapper
        return decorator
        
    def memoize_cache (
        self,
    ) -> None:
        
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.memoize_caching.cache (
                    func,  
                    *args, 
                    **kwargs
                )
            return wrapper
        return decorator
        
    def lru_cache (
        self,
    ) -> None:
        
        pass