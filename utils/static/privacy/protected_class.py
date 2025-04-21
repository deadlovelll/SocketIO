"""
Protected Class Utility

This module defines `ProtectedClass`, a base class that enforces restricted access
to internal attributes (those starting with a single underscore `_`). If such attributes
are accessed externally (i.e., not from within the class instance), an exception is raised.

Useful for enforcing encapsulation and access control in complex systems.
"""

import inspect
from typing import Any

from exceptions.static_exceptions.static_exceptions import SocketIOStaticAccessException


class ProtectedClass:
    
    """
    Base class that prevents access to protected attributes from outside the instance.

    Attributes prefixed with a single underscore (e.g., `_internal_state`) are considered
    protected and should only be accessed from within the class itself.

    Raises:
        SocketIOStaticAccessException: If a protected attribute is accessed externally.
    """

    def __getattribute__ (
        self, 
        name: str,
    ) -> Any:
        
        """
        Override attribute access to enforce protection of `_`-prefixed fields.

        Args:
            name (str): The name of the attribute being accessed.

        Returns:
            Any: The value of the attribute if access is permitted.

        Raises:
            SocketIOStaticAccessException: If external code tries to access a protected attribute.
        """
        
        if name.startswith('_') and not name.startswith('__'):
            stack = inspect.stack()
            try:
                caller_frame = stack[1].frame
                caller_self = caller_frame.f_locals.get('self')
                if caller_self is not self:
                    raise SocketIOStaticAccessException(name)
            finally:
                del stack  
        return super().__getattribute__(name)
