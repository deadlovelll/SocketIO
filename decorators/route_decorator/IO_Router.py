from typing import Callable

class IORouter:
    
    def __init__ (
        self
    ) -> None:
        
        self.routes = []
    
    def route (
        self, 
        path,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None]
        ) -> Callable[..., None]:
            
            self.routes[path] = handler
            return handler
        return wrapper