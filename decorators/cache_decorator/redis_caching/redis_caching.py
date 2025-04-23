"""
RedisCaching module.

Provides a Redis-based caching mechanism to store and retrieve
results of function calls with expiration control. This implementation
is useful for distributed caching scenarios where performance
and scalability are critical.

Depends on:
    - redis-py: for communication with the Redis server.
    - pickle: for serializing complex Python objects.
    - hashlib: for generating unique and safe cache keys.

Raises:
    - NoRedisConfiguredException: If the Redis client is not configured.
"""

import redis
import pickle
import hashlib
from typing import Callable, Any

from decorators.cache_decorator.redis_caching.redis_config import RedisConfig
from exceptions.redis_exceptions.no_redis_configured_exception import NoRedisConfiguredException


class RedisCaching:
    
    """
    Redis-based function result caching class.

    Attributes:
        redis_client (redis.Redis): Redis client instance initialized from RedisConfig.
    """

    def __init__ (
        self,
        redis_config: RedisConfig = None,
    ) -> None:
        
        """
        Initializes RedisCaching with an optional Redis configuration.

        Args:
            redis_config (RedisConfig, optional): Configuration object for Redis connection.
        """
        
        self.redis_client = self.__init_redis(redis_config)

    def __init_redis (
        self,
        redis_config: RedisConfig,
    ) -> redis.Redis:
        
        """
        Initializes the Redis client from the given configuration.

        Args:
            redis_config (RedisConfig): Redis connection configuration.

        Returns:
            redis.Redis: A Redis client instance.
        """
        
        if redis_config:
            return redis.Redis(**redis_config._asdict())
        return None

    def cache (
        self, 
        func: Callable[..., Any], 
        duration: int, 
        *args: Any, 
        **kwargs: Any,
    ) -> Any:
        
        """
        Caches the result of a function call in Redis.

        Args:
            func (Callable): The function whose result is to be cached.
            duration (int): Expiration time for the cached result in seconds.
            *args (Any): Positional arguments passed to the function.
            **kwargs (Any): Keyword arguments passed to the function.

        Returns:
            Any: The result of the function call, either from cache or computed.
        
        Raises:
            NoRedisConfiguredException: If Redis is not configured.
        """
        
        if not self.redis_client:
            raise NoRedisConfiguredException()

        key = f"cache:{func.__name__}:{pickle.dumps((args, kwargs))}"
        cached_result = self.redis_client.get(key)

        if cached_result:
            return pickle.loads(cached_result)

        result = func(*args, **kwargs)
        self.redis_client.setex(key, duration, pickle.dumps(result))
        return result

    def _generate_cache_key (
        self,
        func_name: str,
        args: tuple,
        kwargs: dict[str, Any],
    ) -> str:
        
        """
        Generates a unique hash-based cache key using function name and arguments.

        Args:
            func_name (str): The name of the function.
            args (tuple): Function positional arguments.
            kwargs (dict): Function keyword arguments.

        Returns:
            str: A SHA-256 hash string representing the cache key.
        """
        
        key_data = f"{func_name}:{args}:{kwargs}"
        return hashlib.sha256(key_data.encode()).hexdigest()
