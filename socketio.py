import asyncio
import os
import sys
import socket
import psutil
import signal
import threading

from autodoc.autodoc import AutoDocGenerator

from decorators.lifecycle_hooks.lifecycle_hooks import LifecycleHooks
from decorators.rate_limit_decorator.rate_limit import RateLimitation
from decorators.async_decorator.async_decorator import AsyncDecorator
from decorators.cache_decorator.cache_decorator import CacheDecorator
from decorators.route_decorator.IO_Router import IORouter
from decorators.middleware.middleware import IOMiddleware
from decorators.bound_handlers.bound_handlers import BoundHandlers

from file_wacther.file_watcher import FileWatcher

class SocketIO:
    
    def __init__ (
        self, 
        host="127.0.0.1", 
        port=4000,
        redis_server=None,
        backlog=5
    ):
        
        self.running = False
        self.host = host
        self.port = port
        self.server_socket = None
        self.backlog = backlog
        self.threads = []
        
        # Decorators
        self.life_cycle_hooks_handler = LifecycleHooks()
        self.rate_limitation_handler = RateLimitation()
        self.async_handler = AsyncDecorator()
        self.bound_handler = BoundHandlers()
        self.cache_handler = CacheDecorator()
        self.IORouter = IORouter()
        self.IOMiddleware = IOMiddleware()
        
        self.openapi_paths = {}

    def _create_property(attr_path: str):
        """Helper function to create a dynamic property"""
        return property(lambda self: eval(f"self.{attr_path}"))

    # Dynamically define properties
    route = _create_property("IORouter.route")
    IOBound = _create_property("bound_handler.IOBound")
    CPUBound = _create_property("bound_handler.CPUBound")
    rate_limit = _create_property("rate_limitation_handler.rate_limit")
    on_start = _create_property("life_cycle_hooks_handler.on_start")
    on_shutdown = _create_property("life_cycle_hooks_handler.on_shutdown")
    cache = _create_property("cache_handler.cache")
    
    async def serve (
        self,
    ):  
        await self.register_signal_handlers()
        
        self.running = True
        self.server_socket = socket.socket (
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt (
            socket.SOL_SOCKET, 
            socket.SO_REUSEADDR, 
            1,
        )
        self.server_socket.bind (
            (self.host, self.port)
        )
        self.server_socket.listen(self.backlog)
        
        print(f"Server running on {self.host}:{self.port}")
        
        watcher_thread = threading.Thread(
            target=FileWatcher(["."], self.restart_server).start,
            daemon=True
        )
        watcher_thread.start()

        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread (
                    target=self.IORouter.handle_request, 
                    args=(client_socket,)
                )
                client_thread.start()
                self.threads.append(client_thread)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            await self.shutdown()
            
    async def register_signal_handlers(self):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler (
                sig, 
                lambda: asyncio.create_task(self.shutdown(sig))
            )
    
    async def shutdown (
        self,
    ) -> None:
        
        self.running = False

        if self.server_socket:
            self.server_socket.close()

        for thread in self.threads:
            thread.join()

        current_process = psutil.Process(os.getpid())
        current_process.terminate()
        os._exit(0)
        
    async def restart_server (
        self,
    ) -> None:
        
        os.execv(sys.executable, [sys.executable] + sys.argv)