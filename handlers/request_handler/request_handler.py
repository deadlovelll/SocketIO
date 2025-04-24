"""
This module defines a `RequestHandler` class responsible for handling incoming HTTP and WebSocket requests.
It processes requests, verifies the host, and delegates the handling of WebSocket and HTTP requests to their respective handlers.
"""

import socket
from urllib.parse import urlparse
from typing import Any

from handlers.http_handler.http_handler import HTTPHandler
from handlers.websocket_handler.websocket_handler import WebsocketHandler

from parsers.request_parser.request_parser import RequestParser

from utils.static.privacy.privacy import privatemethod
from utils.static.privacy.protected_class import ProtectedClass

class RequestHandler(ProtectedClass):
    
    """
    A handler for processing HTTP and WebSocket requests. It verifies the host, parses the request data,
    and delegates the processing to appropriate handlers based on the request type (HTTP or WebSocket).
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the `RequestHandler` with instances of WebSocket and HTTP handlers.

        Args:
            None
        """
        
        self._websocket_handler = WebsocketHandler()
        self._http_handler = HTTPHandler()
    
    async def handle_request (
        self, 
        client_socket: socket.socket,
        http_routes: dict[str, Any],
        websocket_routes: dict[str, Any],
        allowed_hosts: list[int],
    ) -> None:
        
        """
        Handles an incoming request by verifying the host, parsing the request, 
        and delegating it to either the WebSocket or HTTP handler.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.
            http_routes (dict): A dictionary of available HTTP routes for handling requests.
            websocket_routes (dict): A dictionary of available WebSocket routes for handling requests.
            allowed_hosts (list): A list of allowed IP addresses for the client.

        Returns:
            None
        """
        
        try:
            request_data = await self._read_request(client_socket)
            if not request_data:
                return
            
            if not await (
                self._verify_host (
                    client_socket, 
                    allowed_hosts,
                )
            ):
                client_socket.close()
                return

            request_line, headers = RequestParser.parse_request(request_data)
            method, path, _ = request_line.split(' ')
            parsed_path = urlparse(path)
            
            if self._is_websocket_request(headers):
                await self._websocket_handler.handle_websocket (
                    client_socket, 
                    request_data, 
                    headers, 
                    websocket_routes,
                )
            else:
                await self._http_handler.handle_http_request (
                    request_data, 
                    path, 
                    parsed_path, 
                    client_socket, 
                    http_routes,
                )
            
        except Exception as e:
            print(f'Error processing request: {e}')
        finally:
            client_socket.close()

    @privatemethod
    async def _read_request (
        self,
        client_socket: socket.socket,
    ) -> str:
        
        """
        Reads data from the client socket.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.

        Returns:
            str: The data read from the socket, decoded as a string, or an empty string if an error occurs.
        """
        
        try:
            return client_socket.recv(1024).decode().strip()
        except Exception:
            return ''
    
    @privatemethod
    async def _verify_host (
        self, 
        client_socket: socket.socket,
        allowed_hosts: list,
    ) -> bool:
        
        """
        Verifies if the client's IP address is in the allowed hosts list.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.
            allowed_hosts (list): A list of allowed IP addresses.

        Returns:
            bool: `True` if the client's IP is in the allowed hosts list, otherwise `False`.
        """
        
        ip, port = client_socket.getpeername()
        return ip in allowed_hosts
    
    @privatemethod
    def _is_websocket_request (
        self,
        headers: dict[str, Any],
    ) -> bool:
        
        """
        Checks if the request is a WebSocket upgrade request based on the headers.

        Args:
            headers (dict): The headers of the incoming request.

        Returns:
            bool: `True` if the request is a WebSocket upgrade request, otherwise `False`.
        """
        
        return 'Upgrade' in headers and headers['Upgrade'].lower() == 'websocket'
        
    