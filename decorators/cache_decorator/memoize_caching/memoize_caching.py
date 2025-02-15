import functools
from typing import Callable, Any

class MemoizeCaching:
    
    def __init__ (
        self,
    ) ->  None:
        
        self.cache_d = {}

    def cache (
        self, 
        func: Callable, 
        *args: Any, 
        **kwargs: Any,
    ):
        key = (
            func.__name__, 
            args, 
            frozenset(kwargs.items())
        )
        
        if key in self.cache_d:
            return self.cache_d[key]
        
        result = func(*args, **kwargs)
        self.cache_d[key] = result
        
        return result