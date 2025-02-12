import asyncio

from urllib.parse import urlparse
from typing import Callable

class IORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
    
    def route (
        self, 
        path,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.routes[path] = handler
            return handler
        return wrapper
    
    async def handle_request (
        self, 
        reader, 
        writer,
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