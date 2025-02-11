from typing import Callable

class IORouter:
    
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