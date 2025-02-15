import redis
import pickle
import hashlib
from typing import Callable

from decorators.cache_decorator.redis_caching.redis_config import RedisConfig
from exceptions.redis_exceptions.no_redis_configured_exception import NoRedisConfiguredException

class RedisCaching:
    
    def __init__ (
        self,
        redis_config: RedisConfig = None
    ) -> None:
        
        self.redis_client = redis.Redis (
            **redis_config._asdict()
        )
        
    def cache (
        self, 
        duration: int
    ):
        """Cache function results in Redis for a given duration (seconds)."""
        
        if not self.redis_client:
            raise NoRedisConfiguredException()
        
        def decorator (
            func: Callable[..., str]
        ) -> Callable[..., str]:
            
            def wrapper (
                *args, 
                **kwargs
            ):
                # Generate a unique cache key based on function name & arguments
                key = self._generate_cache_key (
                    func.__name__, 
                    args, 
                    kwargs,
                )
                
                # Check if result is in Redis
                cached_result = self.redis_client.get(key)
                if cached_result:
                    return pickle.loads(cached_result)  # Deserialize from Redis

                # Compute the function result
                result = func(*args, **kwargs)

                # Store in Redis with expiration
                self.redis_client.setex(key, duration, pickle.dumps(result))
                return result
            
            return wrapper
        return decorator
    
    def _generate_cache_key (
        self,
        func_name: str,
        args: tuple,
        kwargs: dict,
    ) -> None:
        
        key_data = f"{func_name}:{args}:{kwargs}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    