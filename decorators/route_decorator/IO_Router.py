import asyncio
import socket

from typing import Callable

from handlers.request_handler.request_handler import RequestHandler
from route_registry.router_registry import RouteRegistry

class IORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.request_handler = RequestHandler()
        self.router_registry = RouteRegistry()
    
    def route (
        self, 
        path: str, 
        methods: list[str] = ['GET'],
        protected: bool = True,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.router_registry.add_route (
                path,
                handler,
                methods,
                protected,
            )
            return handler
        return wrapper
    
    def websocket (
        self, 
        path: str,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.router_registry.websockets[path] = handler
            return handler
        return wrapper   
    
    def handle_request (
        self, 
        client_socket: socket.socket,
        allowed_hosts: list,
    ) -> None:
        
        asyncio.run(self.request_handler.handle_request(
            client_socket,
            self.router_registry.routes,
            self.router_registry.websockets,
            allowed_hosts,
        ))