from typing import OrderedDict, Callable, Any

class LRUCaching:
    
    def __init__ (
        self, 
        max_size: int = 128
    ) -> None:
        
        self.cache_d = OrderedDict()
        self.max_size = max_size

    def get (
        self, 
        key: str
    ):
        if key not in self.cache_d:
            return None
        
        # Move key to end (most recently used)
        self.cache_d.move_to_end(key)
        return self.cache_d[key]

    def put (
        self, 
        key: str, 
        value: Any
    ) -> None:
        
        if key in self.cache_d:
            self.cache_d.move_to_end(key)
            
        elif len(self.cache_d) >= self.max_size:
            self.cache_d.popitem(last=False)  # Remove the least recently used item
            
        self.cache_d[key] = value
        
    def cache (
        self,
        func: Callable, 
        *args: Any,
        **kwargs: Any
    ):
        
        key = (args, frozenset(kwargs.items()))
        cached_result = self.cache_d.get(key)
        
        if cached_result is not None:
            return cached_result
        
        result = func(*args, **kwargs)
        self.cache_d.put(key, result)
        
        return result