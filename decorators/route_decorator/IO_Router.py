import re
import asyncio

from urllib.parse import urlparse
from typing import Callable

from exceptions.handler_exceptions.invalid_rest_operation_type import InvalidRestOperationType

from parsers.request_parser.request_parser import RequestParser
from handlers.websocket_handler.websocket_handler import WebsocketHandler
from handlers.http_handler.http_handler import HTTPHandler

class IORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
        self.websockets = {}
        
        self.websocket_handler = WebsocketHandler()
        self.http_handler = HTTPHandler()
        
    def __convert_path_to_regex (
        self,
        path: str
    ) -> str:
        
        return "^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$"
    
    def route (
        self, 
        path: str, 
        methods: list[str] = ['GET'],
        protected: bool = True,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            if "<" in path and ">" in path:
                regex = self.__convert_path_to_regex(path)
                self.routes[regex] = {
                    'handler': handler,
                    'methods': methods,
                    'dynamic': True,
                    'original': path,
                    'protected': protected
                }
            else:
                if path not in self.routes:
                    self.routes[path] = {}
                self.routes[path]['handler'] = handler
                self.routes[path]['methods'] = methods
                self.routes[path]['dynamic'] = False
                self.routes[path]['protected'] = protected
            return handler
        return wrapper
    
    def websocket (
        self, 
        path,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.websockets[path] = handler
            return handler
        return wrapper   
    
    def handle_request (
        self, 
        client_socket
    ):
        
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                return
            
            if not asyncio.run(self.__verify_host(client_socket)):
                client_socket.close()

            request_line = data.splitlines()[0]
            method, path, _ = request_line.split(" ")
            parsed_path = urlparse(path)
            
            headers = RequestParser.parse_headers(data)
            
            if "Upgrade" in headers and headers["Upgrade"].lower() == "websocket":
                self.websocket_handler.handle_websocket (
                    client_socket, 
                    data, 
                    headers,
                )
                return
            
            else:
                self.http_handler.handle_http_request (
                    data, 
                    path, 
                    parsed_path, 
                    client_socket,
                    self.routes,
                )
        
        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            client_socket.close()
    
    async def __verify_host (
        self, 
        client_socket,
    ):
        ip, port = client_socket.getpeername()
        
        return ip in self.allowed_hosts