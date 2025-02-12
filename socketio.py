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

    async def handle_request (
        self, 
        reader, 
        writer
    ) -> None:
        
        data = await reader.read(1024)
        request_line = data.decode('utf-8').splitlines()[0]
        method, path, _ = request_line.split(" ")
        parsed_path = urlparse(path)

        handler = self.IORouter.routes.get(parsed_path.path)
        
        if parsed_path.path == "/docs":
            response_body = self.serve_swagger_ui()
            status_line = "HTTP/1.1 200 OK\r\n"
            response = f"{status_line}Content-Type: text/html\r\n\r\n{response_body}"
            writer.write(response.encode('utf-8'))
            await writer.drain()
            writer.close()
            return

        if handler:
            try:
                if asyncio.iscoroutinefunction(handler):
                    response_body = await handler()
                elif handler in self.task_type:
                    response_body = await self.run_in_executor(handler)
                else:
                    response_body = handler()  
                status_line = "HTTP/1.1 200 OK\r\n"
            except Exception as e:
                response_body = f"500 Internal Server Error: {e}"
                status_line = "HTTP/1.1 500 Internal Server Error\r\n"
        else:
            response_body = "404 Not Found"
            status_line = "HTTP/1.1 404 Not Found\r\n"

        response = f"{status_line}Content-Type: text/plain\r\n\r\n{response_body}"
        writer.write(response.encode('utf-8'))
        await writer.drain()
        writer.close()

    async def serve (
        self, 
        host="127.0.0.1", 
        port=8000,
    ) -> None:
        
        await self.life_cycle_hooks_handler.run_on_start_handlers()
        server = await asyncio.start_server (
            self.handle_request, 
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
            

