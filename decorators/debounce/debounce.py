"""
This module provides a `Debounce` class that implements a debouncing mechanism for functions.

The debouncing mechanism ensures that a function is only executed after a specified wait time
has passed since the last call. This is particularly useful in scenarios where you want to 
delay the execution of a function until the user stops triggering an event, such as input 
field changes or button presses, to prevent excessive function calls.
"""

import threading
import functools
from typing import Callable, Any


class Debounce:
    
    """
    A class to implement a debounce functionality that delays the execution 
    of a function until after a specified wait time has passed since the last
    call.
    """

    def debounce (
        self,
        wait: float,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        """
        A decorator that delays the execution of the wrapped function until
        after the specified wait time has passed since the last call.

        Args:
            wait (float): The amount of time (in seconds) to wait before invoking 
                          the wrapped function.

        Returns:
            Callable[[Callable[..., None]], Callable[..., None]]:
                A decorator that can be applied to a function to debounce it.
        """
        
        def decorator (
            fn: Callable[..., None],
        ) -> Callable[..., None]:
            
            """
            A decorator that delays the execution of the wrapped function 
            until the specified wait time has passed.

            Args:
                fn (Callable[..., None]): The function to be debounced.

            Returns:
                Callable[..., None]: The debounced version of the function.
            """
            
            timer: threading.Timer | None = None

            @functools.wraps(fn)
            def debounced (
                *args: Any, 
                **kwargs: Any,
            ) -> None:
                
                nonlocal timer
                if timer is not None:
                    timer.cancel()
                    
                timer = threading.Timer(wait, lambda: fn(*args, **kwargs))
                timer.start()

            return debounced
        return decorator
