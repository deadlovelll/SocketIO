"""
MemoizeCaching module.

Provides a simple memoization utility that caches function results based on
the combination of function name, arguments, and keyword arguments.
This is useful for optimizing pure functions with deterministic outputs.
"""

from typing import Callable, Any


class MemoizeCaching:
    
    """
    Basic memoization cache for storing results of function calls.

    Useful for reducing repeated computations by caching the results
    of functions with the same input arguments.

    Attributes:
        cache_d (dict): Dictionary used to store cached results keyed by function name and arguments.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the memoization cache.
        """
        
        self.cache_d = {}

    def cache(
        self, 
        func: Callable, 
        *args: Any, 
        **kwargs: Any,
    ) -> Any:
        
        """
        Returns the cached result of a function call if available, otherwise computes and stores it.

        Args:
            func (Callable): The function whose result should be cached.
            *args (Any): Positional arguments passed to the function.
            **kwargs (Any): Keyword arguments passed to the function.

        Returns:
            Any: The result of the function call, either from cache or newly computed.
        """
        
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