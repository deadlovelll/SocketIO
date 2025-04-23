"""
This module defines the `SocketIORouter` class for managing and registering API routes and WebSocket routes
within the SocketIO framework.
"""

from route_registry.router_registry import RouteRegistry
from configs.route_config.route_config import RouteConfig


class SocketIORouter:
    
    """
    A class for managing and registering API and WebSocket routes in the SocketIO framework.

    Attributes:
        router_registry (RouteRegistry): An instance of `RouteRegistry` to manage registered routes.

    Methods:
        add_api_route(config: RouteConfig):
            Registers an API route based on the given `RouteConfig`.
        
        add_websocket_router(config: RouteConfig):
            Registers a WebSocket route based on the given `RouteConfig`.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the `SocketIORouter` by creating an instance of `RouteRegistry`.
        """
        
        self.router_registry = RouteRegistry()
    
    async def add_api_route (
        self,
        config: RouteConfig,
    ) -> None:
        
        """
        Registers an API route using the configuration provided in the `RouteConfig` object.

        Args:
            config (RouteConfig): The configuration object that contains route details (e.g., path, method, handler).
        """
        
        self.router_registry.add_route (
            **config.__dict__,
        )
        
    async def add_websocket_router (
        self,
        config: RouteConfig,
    ) -> None:
        
        """
        Registers a WebSocket route using the configuration provided in the `RouteConfig` object.

        Args:
            config (RouteConfig): The configuration object that contains route details (e.g., path, method, handler).
        """
        
        self.router_registry.add_websocket_route (
            **config.__dict__,
        )