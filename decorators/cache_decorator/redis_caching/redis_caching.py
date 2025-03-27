import redis
import pickle
import hashlib
from typing import Callable, Any

from decorators.cache_decorator.redis_caching.redis_config import RedisConfig
from exceptions.redis_exceptions.no_redis_configured_exception import NoRedisConfiguredException

class RedisCaching:
    
    def __init__ (
        self,
        redis_config: RedisConfig = None
    ) -> None:
        
        self.redis_client = self.__init_redis (
            redis_config
        )
        
    def __init_redis (
        self,
        redis_config,
    ):
        if redis_config:
            return redis.Redis (
                **redis_config._asdict()
            )
        
        return None
        
    def cache (
        self, 
        func: Callable[..., Any], 
        duration: int, 
        *args: Any, 
        **kwargs: Any
    ):
        
        """Handles caching logic for Redis."""
        
        if not self.redis_client:
            raise NoRedisConfiguredException()

        key = f"cache:{func.__name__}:{pickle.dumps((args, kwargs))}"
        cached_result = self.redis_client.get(key)

        if cached_result:
            return pickle.loads(cached_result) 

        result = func (
            *args, 
            **kwargs
        )
        self.redis_client.setex (
            key, 
            duration, 
            pickle.dumps(result)
        )  
        return result
    
    def _generate_cache_key (
        self,
        func_name: str,
        args: tuple,
        kwargs: dict,
    ) -> str:
        
        key_data = f"{func_name}:{args}:{kwargs}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    