"""
Module for handling the preparation and setup of a SocketIO server.

This module contains the `PreparationHandler` class, which is responsible for preparing the server 
by performing several key tasks:
  - Registering signal handlers for graceful shutdown.
  - Binding a TCP socket to the specified host and port.
  - Displaying a welcome message with server details.
  - Starting a file observer to watch for file changes and trigger a server restart.

The `PreparationHandler` class assumes the existence of several attributes in the consuming class, 
such as host, port, backlog, running flag, and methods for restarting and shutting down the server.
"""

import asyncio
import signal
import socket
import threading

from file_wacther.file_watcher import FileWatcher

from utils.static.privacy.privacy import privatemethod


class PreparationHandler:
    
    """
    A helper class that performs the initial preparation required to set up the SocketIO server.
    
    This includes:
      - Registering signal handlers for graceful shutdown.
      - Binding a TCP socket to the specified host and port.
      - Displaying a welcome message with server details.
      - Starting a file observer to watch for file changes and trigger a server restart.
    
    Note:
      The class assumes that the following attributes are defined in the consuming class:
        - self.host: The server host.
        - self.port: The server port.
        - self.backlog: The maximum number of queued connections.
        - self.running: A flag indicating whether the server is running.
        - self.server_socket: The socket instance.
        - self.restart: A method to restart the server.
        - self.shutdown: A method to shut down the server.
    """
    
    async def prepare (
        self,
    ) -> None:
        
        """
        Perform all preparation steps to initialize the server.

        This method sequentially calls internal methods to:
          - Register signal handlers.
          - Bind the server socket.
          - Display a welcome message.
          - Start the file observer.

        Raises:
            Exception: Propagates any exceptions raised during the preparation steps.
        """
        
        await self._register_signal_handlers()
        await self._bind_socket()
        await self._print_hello_message()
        await self._start_file_observer()
    
    @privatemethod
    async def _register_signal_handlers (
        self,
    ) -> None:
        
        """
        Register OS signal handlers for graceful shutdown.

        This method sets up signal handlers for SIGINT and SIGTERM. When these signals
        are received, the server's shutdown method is scheduled to run asynchronously.

        Note:
            The consuming class must define a shutdown method that accepts a signal parameter.
        """
        
        loop = asyncio.get_running_loop()
        
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler (
                sig, 
                lambda: asyncio.create_task(self.shutdown(sig))
            )
    
    @privatemethod
    async def _bind_socket (
        self,
    ) -> None:
        
        """
        Bind a TCP socket to the specified host and port.

        This method:
          - Marks the server as running.
          - Creates a new socket with IPv4 and TCP.
          - Configures the socket to allow address reuse.
          - Binds the socket to (self.host, self.port).
          - Starts listening for incoming connections with a defined backlog.

        Raises:
            OSError: If the socket cannot be bound to the specified address.
        """
        
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
    
    @privatemethod 
    async def _print_hello_message (
        self,
    ) -> None:
        
        print('Wecolme to SocketIO!')
        print(f"HTTP Server running on http://{self.host}:{self.port}")            
        if getattr(self, 'grpc_port', None):
            print(f"gRPC Server running on {self.host}:{self.grpc_port}")
        print('Quit the server with CONTROL-C.')
    
    @privatemethod  
    async def _start_file_observer (
        self,
    ) -> None:
        
        """
        Display a welcome message with server connection details.

        The message includes:
          - A welcome note.
          - The URL where the server is running.
          - Instructions for how to stop the server.
        """
        
        watcher_thread = threading.Thread (
            target=FileWatcher(["."], self.restart).start,
            daemon=True
        )
        watcher_thread.start()