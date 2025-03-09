import asyncio
import socket

from typing import Callable

from exceptions.handler_exceptions.invalid_rest_operation_type import InvalidRestOperationType

class HTTPHandler:
    
    def __init__(self) -> None:
        pass
    
    async def handle_http_request (
        self, 
        data: str, 
        path: str, 
        parsed_path: str, 
        client_socket: socket.socket,
        http_routes: dict,
    ) -> None:
        
        if parsed_path.path == "/favicon.ico":
            return

        try:
            self.__verify_rest_method(data, path)
            handler = self.get_handler (
                parsed_path.path,
                http_routes
            )

            if handler:
                response_body = await self.execute_handler(handler)
                status_line = "HTTP/1.1 200 OK\r\n"
            else:
                response_body = "404 Not Found"
                status_line = "HTTP/1.1 404 Not Found\r\n"

        except Exception as e:
            response_body = f"500 Internal Server Error: {e}"
            status_line = "HTTP/1.1 500 Internal Server Error\r\n"

        self.send_response (
            client_socket, 
            status_line, 
            response_body,
        )
        
    def get_handler (
        self, 
        path: str,
        http_routes: dict,
    ) -> Callable[..., None]:
        
        route = http_routes.get(path)
        return route['handler'] if route else None

    async def execute_handler (
        self, 
        handler: Callable[..., None],
    ) -> str:

        return await handler() if asyncio.iscoroutinefunction(handler) else handler()

    def send_response (
        self, 
        client_socket: socket.socket, 
        status_line: str, 
        body: str,
    ) -> None:

        response = f"{status_line}Content-Type: text/plain\r\n\r\n{body}"
        client_socket.sendall(response.encode())
        
    
    def __verify_rest_method (
        self,
        data: str,
        parsed_path: str,
        http_routes: dict
    ) -> None:
        
        operation_type = data.split('\n')[0].split('/')[0].strip(' ')
        if operation_type not in http_routes[parsed_path]['methods']:
            raise InvalidRestOperationType (
                http_routes.get(parsed_path.path)['methods'],
                operation_type,  
            ) 