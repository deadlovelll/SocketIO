"""
This module provides the `RateLimitation` class for enforcing rate limits 
on function calls. The class allows you to specify the maximum number of 
calls that can be made to a function within a given time interval.

The `rate_limit` decorator can be used to limit the number of times a 
function can be called in a specified time window. If the function exceeds 
the allowed number of calls within the interval, an exception is raised.
"""

import time
from typing import Any, Callable

class RateLimitation:
    
    """
    A class to apply rate limiting to function calls, restricting the number 
    of calls that can be made within a specified time interval.
    """

    def rate_limit(
        self, 
        max_calls: int, 
        interval: int,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        """
        A decorator that enforces a rate limit on a function by restricting 
        the number of calls that can be made within a given time interval.

        Args:
            max_calls (int): The maximum number of allowed function calls within the interval.
            interval (int): The time window (in seconds) during which the calls are counted.

        Returns:
            Callable[[Callable[..., None]], Callable[..., None]]:
                A decorator that limits the rate of function calls.
        """
        
        call_times: list[float] = []

        def decorator(
            func: Callable[..., None],
        ) -> Callable[..., None]:
            
            """
            The actual decorator that wraps the function to apply the rate limit.

            Args:
                func (Callable[..., None]): The function to be rate-limited.

            Returns:
                Callable[..., None]: The wrapped function that applies rate-limiting logic.
            """
            
            def wrapper (
                *args: Any, 
                **kwargs: Any,
            ) -> None:
                
                """
                The wrapper function that checks the rate limit and calls the original function.

                Args:
                    *args: Positional arguments passed to the decorated function.
                    **kwargs: Keyword arguments passed to the decorated function.

                Returns:
                    None: The result of the decorated function is returned.
                
                Raises:
                    Exception: If the rate limit is exceeded, an exception is raised.
                """
                
                now: float = time.time()
                call_times.append(now)
                # Keep only the call timestamps within the interval
                call_times[:] = [t for t in call_times if now - t < interval]

                if len(call_times) > max_calls:
                    raise Exception("Rate limit exceeded")

                return func(*args, **kwargs)

            return wrapper
        return decorator
