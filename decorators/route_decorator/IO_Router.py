import re
import asyncio
import socket

from urllib.parse import urlparse
from typing import Callable

from exceptions.handler_exceptions.invalid_rest_operation_type import InvalidRestOperationType

from parsers.request_parser.request_parser import RequestParser
from handlers.request_handler.request_handler import RequestHandler

class IORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
        self.websockets = {}
        
        self.request_handler = RequestHandler()
        
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
        path: str,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.websockets[path] = handler
            return handler
        return wrapper   
    
    def handle_request (
        self, 
        client_socket: socket.socket,
        allowed_hosts: list,
    ) -> None:
        
        asyncio.run(self.request_handler.handle_request(
            client_socket,
            self.routes,
            self.websockets,
            allowed_hosts,
        ))