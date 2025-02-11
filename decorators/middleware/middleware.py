from typing import Callable

class IOMiddleware:
    
    def __init__ (
        self
    ) -> None:
        
        self.before_request_handlers = []
        self.after_request_handlers = []
    
    def before_request (
        self,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None]
        ) -> Callable[..., None]:
            
            self.before_request_handlers.append(handler)
            return handler
        return wrapper
    
    def after_request (
        self,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None]
        ) -> Callable[..., None]:
            
            self.after_request_handlers.append(handler)
            return handler
        return wrapper