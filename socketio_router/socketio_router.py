from route_registry.router_registry import RouteRegistry
from configs.route_config.route_config import RouteConfig

class SocketIORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.router_registry = RouteRegistry()
    
    async def add_api_route (
        self,
        config: RouteConfig,
    ) -> None:
        
        self.router_registry.add_route (
            **config.__dict__,
        )
        
    async def add_websocket_router (
        self,
        config: RouteConfig,
    ) -> None:
        
        self.router_registry.add_websocket_route (
            **config.__dict__,
        )