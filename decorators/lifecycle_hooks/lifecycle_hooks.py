import asyncio
from typing import Callable

class LifecycleHooks:
    
    def __init__ (
        self
    ) -> None:
        
        self.startup_handlers = []
        self.shutdown_handlers = []

    def on_start (
        self
    ) -> Callable[[Callable[[], None]], Callable[[], None]]:
            
        def wrapper (
            handler: Callable[[], None]
        ) -> Callable[[], None]:
            
            self.startup_handlers.append(handler)
            return handler 
        return wrapper


    def on_shutdown (
        self
    ) -> Callable[[Callable[[], None]], Callable[[], None]]:
            
        def wrapper (
            handler: Callable[[], None]
        ) -> Callable[[], None]:
            
            self.shutdown_handlers.append(handler)
            return handler 
        return wrapper
    
    async def run_on_start_handlers (
        self,
    ) -> None:
        
        await asyncio.gather(*[
            handler() if asyncio.iscoroutinefunction(handler) else asyncio.to_thread(handler)
            for handler in self.startup_handlers
        ])

    async def run_on_shutdown_handlers (
        self,
    ) -> None:
        
        await asyncio.gather(*[
            handler() if asyncio.iscoroutinefunction(handler) else asyncio.to_thread(handler)
            for handler in self.shutdown_handlers
        ])
