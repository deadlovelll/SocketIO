"""
LRUCaching module.

Implements a basic Least Recently Used (LRU) cache mechanism using an OrderedDict.
Provides `get`, `put`, and `cache` methods to manually manage cached function results
and ensure that only the most recent `max_size` items are retained.
"""

from typing import OrderedDict, Callable, Any


class LRUCaching:
    
    """
    Least Recently Used (LRU) cache implementation.

    Stores a fixed number of items. When the limit is exceeded, the least recently used
    item is discarded. Suitable for optimizing repeated function calls with the same arguments.
    
    Attributes:
        max_size (int): Maximum number of items to store in the cache.
        cache_d (OrderedDict): Dictionary maintaining order of item usage.
    """
    
    def __init__ (
        self, 
        max_size: int = 128,
    ) -> None:
        
        """
        Initializes the LRU cache.

        Args:
            max_size (int): The maximum number of items to store. Defaults to 128.
        """
        
        self.cache_d = OrderedDict()
        self.max_size = max_size

    def get (
        self, 
        key: str,
    ) -> Any:
    
        """
        Retrieves a value from the cache by key and marks it as recently used.

        Args:
            key (str): The cache key.

        Returns:
            Any: The cached value or None if the key is not present.
        """
        
        if key not in self.cache_d:
            return None
        
        self.cache_d.move_to_end(key)
        return self.cache_d[key]

    def put (
        self, 
        key: str, 
        value: Any,
    ) -> None:
        
        """
        Inserts a value into the cache and evicts the oldest entry if needed.

        Args:
            key (str): The cache key.
            value (Any): The value to store.
        """
        
        if key in self.cache_d:
            self.cache_d.move_to_end(key)
            
        elif len(self.cache_d) >= self.max_size:
            self.cache_d.popitem(last=False)  
            
        self.cache_d[key] = value
        
    def cache (
        self,
        func: Callable, 
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        
        """
        Manages caching for a given function call with provided arguments.

        Args:
            func (Callable): The function to call and possibly cache.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.

        Returns:
            Any: The result of the function, from cache or computed.
        """
        
        key = (args, frozenset(kwargs.items()))
        cached_result = self.cache_d.get(key)
        
        if cached_result is not None:
            return cached_result
        
        result = func(*args, **kwargs)
        self.cache_d.put(key, result)
        
        return result