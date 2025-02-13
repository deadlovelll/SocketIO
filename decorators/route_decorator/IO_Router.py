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
    
    def handle_request(self, client_socket):
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                return

            request_line = data.splitlines()[0]
            method, path, _ = request_line.split(" ")
            parsed_path = urlparse(path)

            handler = self.routes.get(parsed_path.path)
            
            if handler:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        response_body = asyncio.run(handler()) 
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
            client_socket.sendall(response.encode())
        
        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            client_socket.close()