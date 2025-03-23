import re

from typing import Callable, List

class RouteRegistry:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
        self.websockets = {}
        
    def convert_path_to_regex (
        self, 
        path: str,
    ) -> str:
        
        return "^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$"
    
    def add_route (
        self,
        path: str,
        handler: Callable[..., None],
        methods: List[str],
        protected: bool,
    ) -> None:
        
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
        
        self.websockets[path] = handler
