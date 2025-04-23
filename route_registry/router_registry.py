"""
This module defines the `RouteRegistry` class for managing and registering both API routes and WebSocket routes.
It includes functionality for converting path patterns to regular expressions and registering both dynamic and static routes.
"""

import re

from typing import Callable, List


class RouteRegistry:
    
    """
    A class responsible for registering and managing API and WebSocket routes.

    Attributes:
        routes (dict): A dictionary to store static and dynamic API routes with their corresponding handlers.
        websockets (dict): A dictionary to store WebSocket routes with their corresponding handlers.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the `RouteRegistry` with empty dictionaries for routes and websockets.
        """
        
        self.routes = {}
        self.websockets = {}
        
    def convert_path_to_regex (
        self, 
        path: str,
    ) -> str:
        
        """
        Converts a dynamic path pattern (e.g., "/api/v1/<id>") to a regular expression pattern.

        Args:
            path (str): The dynamic route path that may contain placeholders enclosed in "<>".
        
        Returns:
            str: A regular expression pattern representing the dynamic path.
        """
        
        return "^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$"
    
    def add_route (
        self,
        path: str,
        handler: Callable[..., None],
        methods: List[str],
        protected: bool,
    ) -> None:
        
        """
        Registers a new API route with the given path, handler, allowed methods, and protection status.

        Args:
            path (str): The route path, which may be static or dynamic (containing placeholders).
            handler (Callable[..., None]): The handler function to be called when the route is matched.
            methods (List[str]): A list of HTTP methods (e.g., "GET", "POST") allowed for this route.
            protected (bool): A flag indicating whether the route requires protection (e.g., authentication).
        """
        
        if "<" in path and ">" in path:
            regex = self.convert_path_to_regex(path)
            self.routes[regex] = {
                'handler': handler,
                'methods': methods,
                'dynamic': True,
                'original': path,
                'protected': protected
            }
        else:
            self.routes[path] = {
                'handler': handler,
                'methods': methods,
                'dynamic': False,
                'protected': protected
            }
            
    def add_websocket_route (
        self,
        path: str,
        handler: Callable[..., None],
    ) -> None:
        
        """
        Registers a new WebSocket route with the given path and handler.

        Args:
            path (str): The WebSocket route path.
            handler (Callable[..., None]): The handler function to be called when the WebSocket route is matched.
        """
        
        self.websockets[path] = handler
