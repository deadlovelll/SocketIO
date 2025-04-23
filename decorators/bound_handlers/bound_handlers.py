"""
BoundHandlers module.

Provides decorators for executing handlers as IO-bound or CPU-bound tasks,
offloading them to appropriate executor pools (ThreadPoolExecutor for IO,
ProcessPoolExecutor for CPU).

Useful in asynchronous environments for keeping the event loop non-blocking
by isolating heavy operations in separate threads or processes.
"""

from concurrent.futures import (
    ThreadPoolExecutor, 
    ProcessPoolExecutor
)
from asyncio import get_running_loop
from typing import Callable, Any


class BoundHandlers:
    
    """
    A utility class that allows you to classify and manage task execution types 
    (IO-bound or CPU-bound) by wrapping handlers with appropriate executors.

    This helps in offloading blocking or CPU-intensive work from the main event loop.

    Attributes:
        io_executor (ThreadPoolExecutor): Executor used for IO-bound tasks.
        cpu_executor (ProcessPoolExecutor): Executor used for CPU-bound tasks.
        task_type (dict): Maps each wrapped handler to its execution type and label.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the BoundHandlers instance with separate thread and process pools.
        """
        
        self.task_type = {}
        self.io_executor = ThreadPoolExecutor() 
        self.cpu_executor = ProcessPoolExecutor() 
    
    def IOBound(
        self, 
        task_type: str,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        
        """
        Decorator to wrap a handler function as an IO-bound task.

        The function will be executed in a ThreadPoolExecutor asynchronously.

        Args:
            task_type (str): Label describing the category or nature of the IO task.

        Returns:
            Callable: An asynchronous wrapper around the original handler.
        """
        
        def wrapper (
            handler: Callable[..., Any]
        ) -> Callable[..., Any]:
            
            async def wrapped_handler (
                *args, 
                **kwargs
            ) -> Any:
                
                loop = get_running_loop()
                result = await loop.run_in_executor(
                    self.io_executor,
                    lambda: handler(*args, **kwargs)
                )
                return result

            self.task_type[wrapped_handler] = ('io', task_type)
            return wrapped_handler

        return wrapper

    def CPUBound (
        self, 
        task_type: str
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        
        """
        Decorator to wrap a handler function as a CPU-bound task.

        The function will be executed in a ProcessPoolExecutor.

        Args:
            task_type (str): Label describing the category or nature of the CPU task.

        Returns:
            Callable: A wrapper that submits the function to the process pool.
        """
        
        def wrapper (
            handler: Callable[..., Any]
        ) -> Callable[..., Any]:
            
            def wrapped_handler (
                *args, 
                **kwargs
            ):
                return self.cpu_executor.submit(handler, *args, **kwargs)

            self.task_type[wrapped_handler] = ('cpu', task_type)
            return wrapped_handler

        return wrapper
