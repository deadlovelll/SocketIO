"""
This module provides the `IORouter` class for handling HTTP and WebSocket 
routing in an I/O-bound application. The `IORouter` enables registering 
routes for HTTP requests and WebSocket connections and delegates the 
processing of these requests to appropriate handlers.
"""

import asyncio
import socket
from typing import Callable

from handlers.request_handler.request_handler import RequestHandler
from route_registry.router_registry import RouteRegistry


class IORouter:
    
    """
    The IORouter class is responsible for managing both HTTP and WebSocket 
    routing in an I/O-based server. It allows you to define routes and handle 
    incoming requests, while integrating with a request handler and route registry.

    Attributes:
        request_handler (RequestHandler): An instance of RequestHandler to process incoming requests.
        router_registry (RouteRegistry): An instance of RouteRegistry to store and manage route information.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the IORouter instance with a request handler and route registry.
        """
        
        self.request_handler = RequestHandler()
        self.router_registry = RouteRegistry()

    def route (
        self, 
        path: str, 
        methods: list[str] = ['GET'],
        protected: bool = True,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        """
        Registers an HTTP route handler for a specific path and method.

        Args:
            path (str): The path to register the route for.
            methods (list[str], optional): The HTTP methods (e.g., 'GET', 'POST') for this route. Defaults to ['GET'].
            protected (bool, optional): Whether the route is protected (requires authentication). Defaults to True.

        Returns:
            Callable[[Callable[..., None]], Callable[..., None]]: A decorator that registers the handler function for the route.
        """
        
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
        
        """
        Registers a WebSocket route handler for a specific path.

        Args:
            path (str): The WebSocket path to register the handler for.

        Returns:
            Callable[[Callable[..., None]], Callable[..., None]]: A decorator that registers the WebSocket handler.
        """
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.router_registry.websockets[path] = handler
            return handler
        return wrapper

    def handle_request (
        self, 
        client_socket: socket.socket,
        allowed_hosts: list[str],
    ) -> None:
        
        """
        Processes an incoming request by delegating it to the appropriate 
        request handler and routing it to the correct handler.

        Args:
            client_socket (socket.socket): The client socket to interact with.
            allowed_hosts (list[str]): A list of allowed hosts to authorize the request.

        Returns:
            None: The function does not return anything. It processes the request.
        """
        
        asyncio.run(self.request_handler.handle_request(
            client_socket,
            self.router_registry.routes,
            self.router_registry.websockets,
            allowed_hosts,
        ))
