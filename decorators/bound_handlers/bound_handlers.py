from concurrent.futures import (
    ThreadPoolExecutor, 
    ProcessPoolExecutor
)

from typing import Callable

class BoundHandlers:
    
    def __init__ (
        self
    ) -> None:
        
        self.task_type = {}
        
        # Executors
        self.io_executor = ThreadPoolExecutor() 
        self.cpu_executor = ProcessPoolExecutor() 
    
    def IOBound (
        self, 
        task_type
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler
        )  -> Callable[..., None]:
            async def wrapped_handler (
                *args, 
                **kwargs
            ):
                result = await self.io_executor.submit(handler, *args, **kwargs)
                return result

            self.task_type[wrapped_handler] = ('io', task_type)
            return wrapped_handler

        return wrapper

    def CPUBound (
        self, 
        task_type
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler
        ) -> Callable[..., None]:
            def wrapped_handler (
                *args, 
                **kwargs
            ):
                return self.cpu_executor.submit(handler, *args, **kwargs)

            self.task_type[wrapped_handler] = ('cpu', task_type)
            return wrapped_handler

        return wrapper