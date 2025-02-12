import asyncio
from urllib.parse import urlparse
from typing import Any

from autodoc.autodoc import AutoDocGenerator

from decorators.lifecycle_hooks.lifecycle_hooks import LifecycleHooks
from decorators.rate_limit_decorator.rate_limit import RateLimitation
from decorators.async_decorator.async_decorator import AsyncDecorator
from decorators.cache_decorator.cache_decorator import CacheDecorator
from decorators.route_decorator.IO_Router import IORouter
from decorators.middleware.middleware import IOMiddleware
from decorators.bound_handlers.bound_handlers import BoundHandlers

class SocketIO:
    
    def __init__ (
        self,
    ) -> None:
        
        # Decorators
        self.life_cycle_hooks_handler = LifecycleHooks()
        self.rate_limitation_handler = RateLimitation()
        self.async_handler = AsyncDecorator()
        self.bound_handler = BoundHandlers()
        self.cache_handler = CacheDecorator()
        self.IORouter = IORouter()
        self.IOMiddleware = IOMiddleware()
        
        self.openapi_paths = {}

    def _create_property(attr_path: str):
        """Helper function to create a dynamic property"""
        return property(lambda self: eval(f"self.{attr_path}"))

    # Dynamically define properties
    route = _create_property("IORouter.route")
    IOBound = _create_property("bound_handler.IOBound")
    CPUBound = _create_property("bound_handler.CPUBound")
    rate_limit = _create_property("rate_limitation_handler.rate_limit")
    on_start = _create_property("life_cycle_hooks_handler.on_start")
    on_shutdown = _create_property("life_cycle_hooks_handler.on_shutdown")
    cache = _create_property("cache_handler.cache")

    async def run_in_executor (
        self,
        handler, 
        *args
    ) -> None:
        
        task_info = self.task_type.get(handler)
        if task_info:
            task_type, _ = task_info
            executor = self.io_executor if task_type == 'io' else self.cpu_executor
            return await asyncio.wrap_future(executor.submit(handler, *args))
        else:
            return handler(*args)

    async def serve (
        self, 
        host="127.0.0.1", 
        port=8000,
    ) -> None:
        
        await self.life_cycle_hooks_handler.run_on_start_handlers()
        server = await asyncio.start_server (
            self.IORouter.handle_request, 
            host, 
            port
        )
        print(f"Welcome to SocketIO!")
        print(f"Serving on {host}:{port}")
        
        try:
            async with server:
                await server.serve_forever()
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
            
        finally:
            await self.life_cycle_hooks_handler.run_on_shutdown_handlers()
            self.io_executor.shutdown(wait=True)
            self.cpu_executor.shutdown(wait=True)
            print("Server has been shut down cleanly.")
            
    async def shutdown (
        self,
    ) -> None:
        
        pass
            

