from typing import Callable

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
    ) -> None:
        
        self.redis_caching.cache()
        
    def memoize (
        self,
    ) -> None:
        
        self.memoize_caching.memoize()
        
    def lrucache (
        self,
    ) -> None:
        
        pass