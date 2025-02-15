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
from decorators.cache_decorator.cache_decorator import CacheDecorator
from decorators.route_decorator.IO_Router import IORouter
from decorators.middleware.middleware import IOMiddleware
from decorators.bound_handlers.bound_handlers import BoundHandlers
from decorators.auth.auth_handler import AuthHandler

from decorators.cache_decorator.redis_caching.redis_config import RedisConfig

from file_wacther.file_watcher import FileWatcher

class SocketIO:
    
    def __init__ (
        self, 
        host="127.0.0.1", 
        port=4000,
        redis_config: RedisConfig = None,
        public_endpoints=False,
        backlog=5
    ):
        
        self.running = False
        self.host = host
        self.port = port
        self.server_socket = None
        self.backlog = backlog
        self.threads = []
        
        self.redis_config = redis_config
        
        # Decorators
        self.life_cycle_hooks_handler = LifecycleHooks()
        self.rate_limitation_handler = RateLimitation()
        self.bound_handler = BoundHandlers()
        self.cache_handler = CacheDecorator()
        self.IORouter = IORouter()
        self.IOMiddleware = IOMiddleware()
        self.auth_handler = AuthHandler()
        
        self.openapi_paths = {}

    def _create_property(attr_path: str):
        """Helper function to create a dynamic property"""
        return property(lambda self: eval(f"self.{attr_path}"))

    # Dynamically define properties
    route = _create_property("IORouter.route")
    websocket = _create_property("IORouter.websocket")
    
    IOBound = _create_property("bound_handler.IOBound")
    CPUBound = _create_property("bound_handler.CPUBound")
    
    rate_limit = _create_property("rate_limitation_handler.rate_limit")
    on_start = _create_property("life_cycle_hooks_handler.on_start")
    on_shutdown = _create_property("life_cycle_hooks_handler.on_shutdown")
    
    redis_cache = _create_property("cache_handler.redis_cache")
    memoize_cache = _create_property("cache_handler.memoize_cache")
    lru_cache = _create_property("cache_handler.lru_cache")
    
    private_route = _create_property("auth.auth_handler.private_route")
    public_route = _create_property("auth.auth_handler.public_route")
    
    async def serve (
        self,
    ) -> None:
        
        # Preparation for server up
        await self.__prepare()
        
        # Consuming incoming requests
        await self.__consume_requests()
        
    async def restart (
        self,
    ) -> None:
        
        for task in asyncio.all_tasks():
            task.cancel()

        python = sys.executable
        os.execv(python, [python] + sys.argv)
        
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
        
    async def __prepare (
        self,
    ) -> None:
        
        # Registering signal handlers
        await self.__register_signal_handlers()
        
        # Binding server socket
        await self.__bind_socket()
        
        # Displaying hello message
        await self.__print_hello_message()
        
        # Starting file observer
        await self.__start_file_observer()
        
    async def __consume_requests (
        self,
    ) -> None:
        
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
            
    async def __register_signal_handlers (
        self
    ) -> None:
        
        loop = asyncio.get_running_loop()
        
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler (
                sig, 
                lambda: asyncio.create_task(self.shutdown(sig))
            )
        
    async def __bind_socket (
        self,
    ) -> None:
        
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
        
    async def __print_hello_message (
        self,
    ) -> None:
        
        print('Wecolme to SocketIO!')
        print(f"Server running on http://{self.host}:{self.port}")
        print('Quit the server with CONTROL-C.')
        
    async def __start_file_observer (
        self,
    ) -> None:
        
        watcher_thread = threading.Thread(
            target=FileWatcher(["."], self.restart).start,
            daemon=True
        )
        watcher_thread.start()