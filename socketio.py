import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import urlparse


class SocketIO:
    
    def __init__(self):
        self.routes = {}
        self.task_type = {}
        
        self.io_executor = ThreadPoolExecutor()  # For IO-bound tasks
        self.cpu_executor = ProcessPoolExecutor()  # For CPU-bound tasks
        
        self.startup_handlers = []
        self.shutdown_handlers = []

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
    def on_start(self):
        def wrapper(handler):
            self.startup_handlers.append(handler)
            return handler
        return wrapper
    
    def on_shutdown(self, path):
        def wrapper(handler):
            self.shutdown_handlers.append(handler)
            return handler
        return wrapper
    
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

    async def run_in_executor(self, handler, *args):
        task_info = self.task_type.get(handler)
        if task_info:
            task_type, _ = task_info
            executor = self.io_executor if task_type == 'io' else self.cpu_executor
            return await asyncio.wrap_future(executor.submit(handler, *args))
        else:
            return handler(*args)

    async def handle_request(self, reader, writer):
        data = await reader.read(1024)
        request_line = data.decode('utf-8').splitlines()[0]
        method, path, _ = request_line.split(" ")
        parsed_path = urlparse(path)

        handler = self.routes.get(parsed_path.path)

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

    async def serve(self, host="127.0.0.1", port=8000):
        await self.run_on_start_handlers()
        server = await asyncio.start_server(self.handle_request, host, port)
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
            

