import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import urlparse
from typing import Any

from autodoc.autodoc import AutoDocGenerator

from decorators.lifecycle_hooks.lifecycle_hooks import LifecycleHooks
from decorators.rate_limit_decorator.rate_limit import RateLimitation
from decorators.async_decorator.async_decorator import AsyncDecorator
from decorators.cache_decorator.cache_decorator import CacheDecorator
from decorators.route_decorator.IO_Router import IORouter
from decorators.middleware.middleware import IOMiddleware

class SocketIO:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
        self.task_type = {}
        
        self.io_executor = ThreadPoolExecutor()  # For IO-bound tasks
        self.cpu_executor = ProcessPoolExecutor()  # For CPU-bound tasks
        
        # Decorators
        self.life_cycle_hooks_handler = LifecycleHooks()
        self.rate_limitation_handler = RateLimitation()
        self.async_handler = AsyncDecorator()
        self.cache_handler = CacheDecorator()
        self.IORouter = IORouter()
        self.IOMiddleware = IOMiddleware()
        
        self.openapi_paths = {}

    def route (
        self, 
        path,
    ) -> Any:
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
    def generate_openapi(self):
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "SocketIO API",
                "version": "1.0.0"
            },
            "paths": {}
        }
        for path, details in self.openapi_paths.items():
            path_item = {}
            for method, method_details in details["methods"].items():
                path_item[method.lower()] = {
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "responses": method_details["responses"]
                }
            openapi_spec["paths"][path] = path_item
        return openapi_spec
    
    async def run_on_start_handlers(self) -> None:
        for handler in self.startup_handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()
        return None
                
    async def run_on_shutdown_handlers(self):
        for handler in self.shutdown_handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()
        return None

    def IOBound(self, task_type):
        def wrapper(handler):
            async def wrapped_handler(*args, **kwargs):
                result = await self.io_executor.submit(handler, *args, **kwargs)
                return result

            self.task_type[wrapped_handler] = ('io', task_type)
            return wrapped_handler

        return wrapper

    def CPUBound(self, task_type):
        def wrapper(handler):
            def wrapped_handler(*args, **kwargs):
                return self.cpu_executor.submit(handler, *args, **kwargs)

            self.task_type[wrapped_handler] = ('cpu', task_type)
            return wrapped_handler

        return wrapper

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

        handler = self.routes.get(parsed_path.path)
        
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
        
        await self.run_on_start_handlers()
        server = await asyncio.start_server(self.handle_request, host, port)
        self.generate_openapi()
        print(f"Welcome to SocketIO!")
        print(f"Serving on {host}:{port}")
        
        try:
            async with server:
                await server.serve_forever()
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
            
        finally:
            await self.run_on_start_handlers()
            self.io_executor.shutdown(wait=True)
            self.cpu_executor.shutdown(wait=True)
            print("Server has been shut down cleanly.")
            

