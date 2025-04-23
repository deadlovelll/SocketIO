"""
This module provides a `LifecycleHooks` class that manages startup and shutdown handlers 
for asynchronous lifecycle events. The class allows functions to be registered as handlers 
for events such as startup and shutdown, which can be executed in an asynchronous context.

The class supports both regular functions and coroutine functions. Registered handlers 
will be executed during the lifecycle events, and the functions are executed concurrently 
using `asyncio.gather` to handle multiple handlers.
"""

import asyncio
from typing import Callable


class LifecycleHooks:
    
    """
    A class to manage lifecycle hooks for startup and shutdown events.
    
    The `LifecycleHooks` class allows you to register handler functions that 
    will be executed during startup and shutdown. The handlers can be either 
    regular functions or coroutine functions. The class runs all the registered 
    handlers concurrently during the respective lifecycle event.

    Attributes:
        startup_handlers (list): A list to store registered startup handlers.
        shutdown_handlers (list): A list to store registered shutdown handlers.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the LifecycleHooks instance with empty lists for 
        startup and shutdown handlers.
        """
        
        self.startup_handlers = []
        self.shutdown_handlers = []

    def on_start (
        self,
    ) -> Callable[[Callable[[], None]], Callable[[], None]]:
        
        """
        Registers a handler to be called during startup.

        Args:
            handler (Callable[[], None]): A function that will be called during startup.

        Returns:
            Callable[[], None]: The handler function that has been registered.
        """
        
        def wrapper (
            handler: Callable[[], None],
        ) -> Callable[[], None]:
            
            self.startup_handlers.append(handler)
            return handler
        return wrapper

    def on_shutdown (
        self,
    ) -> Callable[[Callable[[], None]], Callable[[], None]]:
        
        """
        Registers a handler to be called during shutdown.

        Args:
            handler (Callable[[], None]): A function that will be called during shutdown.

        Returns:
            Callable[[], None]: The handler function that has been registered.
        """
        
        def wrapper (
            handler: Callable[[], None],
        ) -> Callable[[], None]:
            
            self.shutdown_handlers.append(handler)
            return handler
        return wrapper

    async def run_on_start_handlers (
        self,
    ) -> None:
        
        """
        Executes all registered startup handlers concurrently.
        
        This method will run each startup handler. If the handler is a coroutine 
        function, it will be awaited; otherwise, it will be executed in a separate thread.
        """
        
        await asyncio.gather(*[
            handler() if asyncio.iscoroutinefunction(handler) else asyncio.to_thread(handler)
            for handler in self.startup_handlers
        ])

    async def run_on_shutdown_handlers (
        self,
    ) -> None:
        
        """
        Executes all registered shutdown handlers concurrently.
        
        This method will run each shutdown handler. If the handler is a coroutine 
        function, it will be awaited; otherwise, it will be executed in a separate thread.
        """
        
        await asyncio.gather(*[
            handler() if asyncio.iscoroutinefunction(handler) else asyncio.to_thread(handler)
            for handler in self.shutdown_handlers
        ])
