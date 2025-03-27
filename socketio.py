import asyncio
import os
import sys
import psutil
import grpc

from decorators.lifecycle_hooks.lifecycle_hooks import LifecycleHooks
from decorators.rate_limit_decorator.rate_limit import RateLimitation
from decorators.cache_decorator.cache_decorator import CacheDecorator
from decorators.route_decorator.IO_Router import IORouter
from decorators.middleware.middleware import IOMiddleware
from decorators.bound_handlers.bound_handlers import BoundHandlers
from decorators.cache_decorator.redis_caching.redis_config import RedisConfig

from handlers.__preparation_handler.__preparation_handler import PreparationHandler
from handlers.request_consumer_handler.request_consumer_handler import RequestConsumerHandler
from handlers.grpc_handler.grpc_handler import GRPCHandler

from commands.command_controller.command_controller import CommandController

from utils.socketio_validators.socketio_port_validator.socketio_port_validator import SocketIOPortValidator

class SocketIO (
    PreparationHandler,
    RequestConsumerHandler,
):
    
    def __init__ (
        self, 
        host="127.0.0.1", 
        port=4000,
        redis_config: RedisConfig = None,
        public_endpoints=False,
        grpc_port=None,
        backlog=5
    ) -> None:
        
        """
        Initialize a new SocketIO instance.

        Args:
            host (str, optional): The IP address to bind the server. Defaults to "127.0.0.1".
            port (int, optional): The port on which the server listens. Defaults to 4000.
            redis_config (RedisConfig, optional): Configuration for Redis caching. Defaults to None.
            public_endpoints (bool, optional): Flag to enable public endpoints. Defaults to False.
            backlog (int, optional): The maximum number of queued connections. Defaults to 5.
        """
        
        self.running = False
        self.host = host
        self.port = SocketIOPortValidator.verify_port_validity(port)
        self.server_socket = None
        self.backlog = backlog
        self.threads = []
        
        self.allowed_hosts = ['127.0.0.1']
        self.grpc_port = grpc_port
        self.grpc_server = None
        
        self.redis_config = redis_config
        
        # Decorators
        self.life_cycle_hooks_handler = LifecycleHooks()
        self.rate_limitation_handler = RateLimitation()
        self.bound_handler = BoundHandlers()
        self.cache_handler = CacheDecorator()
        self.IORouter = IORouter()
        self.IOMiddleware = IOMiddleware()
        
        self.openapi_paths = {}
        
    def _create_property (
        attr_path: str,
    ) -> property:
        
        """
        Create a dynamic property for accessing nested attributes.

        This helper function returns a property that retrieves an attribute
        based on a dot-separated attribute path from the instance.

        Args:
            attr_path (str): A string representing the nested attribute path (e.g., "IORouter.route").

        Returns:
            property: A property object that fetches the specified nested attribute.
        """
        
        return property(lambda self: eval(f"self.{attr_path}"))

    # Dynamically defined properties for simplified access to nested attributes
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
    
    async def start (
        self,
    ) -> None:
        
        """
        Prepare and initiate the asynchronous request consumption process.

        This method performs all necessary preparations before entering the main loop
        to consume incoming requests.
        """
        
        await self.prepare()
        if self.grpc_port:
            await self.start_grpc_server()
        else:
            os.environ['GRPC_SERVICE_ENABLED'] = '0'
        await self.consume_requests()
        
    async def start_grpc_server (
        self,
    ) -> None:
        
        """
        Starts the gRPC server dynamically if gRPC support exists.
        """
        
        await GRPCHandler.start_grpc_server (
            grpc_server=self.grpc_server,
            grpc_port=self.grpc_port,
        )
        
    async def restart (
        self,
    ) -> None:
        
        """
        Restart the current process.

        This method cancels all running asyncio tasks and restarts the Python process,
        effectively performing a full application restart.
        """
        
        for task in asyncio.all_tasks():
            task.cancel()

        python = sys.executable
        os.execv(python, [python] + sys.argv)
        
    async def shutdown (
        self,
    ) -> None:
        
        """
        Shutdown the server gracefully.

        This method stops the server from running, closes the server socket if it exists,
        waits for all threads to finish, and finally terminates the current process.
        """
        
        self.running = False

        if self.server_socket:
            self.server_socket.close()

        for thread in self.threads:
            thread.join()

        current_process = psutil.Process(os.getpid())
        current_process.terminate()
        
if __name__ == '__main__':
    CommandController.main()