class LifecycleHooks:
    
    def __init__ (
        self
    ) -> None:
        
        self.startup_handlers = []
        self.shutdown_handlers = []

    def on_start(self):
        """Decorator to register startup handlers"""
        def wrapper(handler):
            self.startup_handlers.append(handler)
            return handler  # Return the original function
        return wrapper

    def on_shutdown(self):
        """Decorator to register shutdown handlers"""
        def wrapper(handler):
            self.shutdown_handlers.append(handler)
            return handler  # Return the original function
        return wrapper
