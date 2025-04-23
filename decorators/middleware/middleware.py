"""
This module provides the `IOMiddleware` class for managing middleware hooks
in an I/O request/response cycle. It allows you to register handler functions
to be executed before and after processing a request. These hooks can be used
to modify or process data before the request reaches the main handler and 
after the request has been processed.
"""

from typing import Callable

class IOMiddleware:
    
    """
    A class to manage middleware hooks for handling I/O requests and responses.

    The `IOMiddleware` class allows registering handler functions that will be 
    executed before and after processing a request. These handlers can perform 
    actions such as logging, modifying request data, or handling response data.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the IOMiddleware instance with empty lists for before and after 
        request handlers.
        """
        
        self.before_request_handlers = []
        self.after_request_handlers = []

    def before_request (
        self,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        """
        Registers a handler to be called before the request is processed.

        Args:
            handler (Callable[..., None]): A function to be executed before 
                                           processing the request.

        Returns:
            Callable[..., None]: The handler function that has been registered.
        """
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.before_request_handlers.append(handler)
            return handler
        return wrapper

    def after_request (
        self,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        """
        Registers a handler to be called after the request is processed.

        Args:
            handler (Callable[..., None]): A function to be executed after 
                                           processing the request.

        Returns:
            Callable[..., None]: The handler function that has been registered.
        """
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.after_request_handlers.append(handler)
            return handler
        return wrapper
