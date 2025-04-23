"""
CacheDecorator module.

Provides a unified interface for different caching strategies: Redis, memoization, and LRU.
This module simplifies the usage of decorators for caching function results based on configuration.
"""

import functools
from typing import Callable, Any

from decorators.cache_decorator.redis_caching.redis_caching import RedisCaching
from decorators.cache_decorator.redis_caching.redis_config import RedisConfig
from decorators.cache_decorator.memoize_caching.memoize_caching import MemoizeCaching
from decorators.cache_decorator.lru_caching.lru_caching import LRUCaching


class CacheDecorator:
    
    """
    Centralized caching decorator provider.

    Supports Redis-based, memoization, and LRU caching mechanisms.
    """

    def __init__ (
        self, 
        redis_config: RedisConfig = None,
    ) -> None:
        
        """
        Initializes the caching backends with optional Redis configuration.

        Args:
            redis_config (RedisConfig, optional): Configuration for Redis caching.
        """
        
        self.redis_config = redis_config
        self.redis_caching = RedisCaching(redis_config)
        self.memoize_caching = MemoizeCaching()
        self.lru_caching = LRUCaching()

    def redis_cache (
        self, 
        duration: int,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        
        """
        Decorator for Redis caching.

        Args:
            duration (int): Time to cache the result in seconds.

        Returns:
            Callable: Wrapped function with Redis-based caching.
        """

        def decorator (
            func: Callable[..., Any],
        ) -> Callable[..., Any]:
            
            @functools.wraps(func)
            def wrapper (
                *args: Any, 
                **kwargs: Any,
            ) -> Any:
                
                return self.redis_caching.cache(
                    func,
                    duration,
                    *args,
                    **kwargs
                )
            return wrapper
        return decorator

    def memoize_cache (
        self,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        
        """
        Decorator for memoization caching (in-memory function-level caching).

        Returns:
            Callable: Wrapped function with memoized caching.
        """

        def decorator (
            func: Callable[..., Any],
        ) -> Callable[..., Any]:
            
            @functools.wraps(func)
            def wrapper (
                *args: Any, 
                **kwargs: Any,
            ) -> Any:
                
                return self.memoize_caching.cache(
                    func,
                    *args,
                    **kwargs
                )
            return wrapper
        return decorator

    def lru_cache (
        self,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        
        """
        Decorator for LRU (Least Recently Used) caching.

        Returns:
            Callable: Wrapped function with LRU caching.
        """

        def decorator (
            func: Callable[..., Any],
        ) -> Callable[..., Any]:
            
            @functools.wraps(func)
            def wrapper (
                *args: Any, 
                **kwargs: Any,
            ) -> Any:
                
                return self.lru_caching.cache(
                    func,
                    *args,
                    **kwargs
                )
            return wrapper
        return decorator
