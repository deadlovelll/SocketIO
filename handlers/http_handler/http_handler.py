"""
This module defines the `HTTPHandler` class, which handles HTTP requests by parsing them, verifying REST methods, 
and sending appropriate responses based on the defined routes.
"""

import asyncio
import socket

from typing import Callable

from exceptions.handler_exceptions.invalid_rest_operation_type import InvalidRestOperationType

from utils.static.privacy.privacy import privatemethod


class HTTPHandler:
    
    """
    A class that handles HTTP requests, verifies REST operation types, executes the corresponding handler,
    and sends responses back to the client.
    """
    
    async def handle_http_request (
        self, 
        data: str, 
        path: str, 
        parsed_path: str, 
        client_socket: socket.socket,
        http_routes: dict,
    ) -> None:
        
        """
        Handles an HTTP request by verifying the method, getting the corresponding handler,
        and sending a response.

        Args:
            data (str): The raw HTTP request data.
            path (str): The path extracted from the HTTP request.
            parsed_path (str): The parsed URL path.
            client_socket (socket.socket): The client socket to send the response.
            http_routes (dict): A dictionary mapping paths to route definitions, including handler functions.

        Returns:
            None
        """
        
        if parsed_path.path == "/favicon.ico":
            return

        try:
            self._verify_rest_method (
                data, 
                path,
                http_routes,
            )
            handler = self._get_handler (
                parsed_path.path,
                http_routes
            )

            if handler:
                response_body = await self._execute_handler(handler)
                status_line = "HTTP/1.1 200 OK\r\n"
            else:
                response_body = "404 Not Found"
                status_line = "HTTP/1.1 404 Not Found\r\n"

        except Exception as e:
            response_body = f"500 Internal Server Error: {e}"
            status_line = "HTTP/1.1 500 Internal Server Error\r\n"

        self._send_response (
            client_socket, 
            status_line, 
            response_body,
        )
    
    @privatemethod
    def _get_handler (
        self, 
        path: str,
        http_routes: dict,
    ) -> Callable[..., None]:
        
        """
        Retrieves the handler function for a given path from the route definitions.

        Args:
            path (str): The path of the HTTP request.
            http_routes (dict): A dictionary mapping paths to route definitions, including handler functions.

        Returns:
            Callable[..., None]: The handler function for the requested path, or None if no handler is found.
        """
        
        route = http_routes.get(path)
        return route['handler'] if route else None

    @privatemethod
    async def _execute_handler (
        self, 
        handler: Callable[..., None],
    ) -> str:
        
        """
        Executes the given handler function, awaiting it if it is asynchronous.

        Args:
            handler (Callable[..., None]): The handler function to be executed.

        Returns:
            str: The response body returned by the handler function.
        """

        return await handler() if asyncio.iscoroutinefunction(handler) else handler()

    @privatemethod
    def _send_response (
        self, 
        client_socket: socket.socket, 
        status_line: str, 
        body: str,
    ) -> None:
        
        """
        Sends the HTTP response back to the client.

        Args:
            client_socket (socket.socket): The client socket to send the response to.
            status_line (str): The status line of the HTTP response (e.g., "HTTP/1.1 200 OK").
            body (str): The body content of the HTTP response.

        Returns:
            None
        """

        response = f"{status_line}Content-Type: text/plain\r\n\r\n{body}"
        client_socket.sendall(response.encode())
        
    @privatemethod
    def _verify_rest_method (
        self,
        data: str,
        parsed_path: str,
        http_routes: dict
    ) -> None:
        
        """
        Verifies if the HTTP request method (e.g., GET, POST) is allowed for the requested path.

        Args:
            data (str): The raw HTTP request data.
            parsed_path (str): The parsed URL path from the HTTP request.
            http_routes (dict): A dictionary of routes and their allowed HTTP methods.

        Raises:
            InvalidRestOperationType: If the HTTP method is not allowed for the requested path.
        """
        
        operation_type = data.split('\n')[0].split('/')[0].strip(' ')
        if operation_type not in http_routes[parsed_path]['methods']:
            raise InvalidRestOperationType (
                http_routes.get(parsed_path.path)['methods'],
                operation_type,  
            ) 