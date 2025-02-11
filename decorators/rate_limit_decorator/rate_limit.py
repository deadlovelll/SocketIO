import time

from typing import Callable

class RateLimitation:

    def rate_limit (
        self, 
        max_calls: int, 
        interval: int
    ):
        call_times = []

        def decorator (
            func: Callable[..., None]
        ) -> Callable[..., None]:
            
            def wrapper (
                *args, 
                **kwargs
            ):
                now = time.time()
                call_times.append(now)
                call_times[:] = [t for t in call_times if now - t < interval]

                if len(call_times) > max_calls:
                    raise Exception("Rate limit exceeded")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator