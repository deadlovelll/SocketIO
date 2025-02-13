import threading
import functools

class Debounce:
    
    def debounce (
        wait: float
    ) -> None:
        
        def decorator(fn):
            timer = None
            
            @functools.wraps
            def debounced(*args, **kwargs):
                nonlocal timer
                if timer is not None:
                    timer.cancel()
                    
                timer = threading.Timer (
                    wait,
                    lambda: fn(*args, **kwargs)
                )
                timer.start()
            return debounced
        return decorator