"""
Private Method Decorator

This module provides a decorator that enforces private method semantics in Python
by restricting access to the method from outside the defining class.
"""

import inspect
from functools import wraps


def privatemethod(method):
    
    """
    Decorator that marks a method as private.

    Ensures the decorated method can only be accessed from within its own class.
    If accessed externally, raises a RuntimeError.

    Args:
        method (Callable): The method to protect.

    Returns:
        Callable: Wrapped method that enforces internal-only access.

    Raises:
        RuntimeError: If the method is accessed from outside the class.
    """
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        stack = inspect.stack()
        for frame_info in stack[1:]:
            caller_self = frame_info.frame.f_locals.get('self')
            if isinstance(caller_self, self.__class__):
                return method(self, *args, **kwargs)
        raise RuntimeError(
            f"Method '{method.__name__}' is private and cannot be accessed externally."
        )
    return wrapper
