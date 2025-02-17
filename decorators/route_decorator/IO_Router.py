import asyncio
import base64
import hashlib

from urllib.parse import urlparse
from typing import Callable

from exceptions.handler_exceptions.invalid_rest_operation_type import InvalidRestOperationType

class IORouter:
    
    def __init__ (
        self,
    ) -> None:
        
        self.routes = {}
        self.websockets = {} 
    
    def route (
        self, 
        path,
        methods=['GET']
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            if path not in self.routes:
                self.routes[path] = {}

            self.routes[path]['handler'] = handler
            self.routes[path]['methods'] = methods
            return handler
        return wrapper
    
    def parse_headers(self, request: str):
        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0].strip()] = parts[1].strip()
        return headers
    
    def handle_request (
        self, 
        client_socket
    ):
        
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                return

            request_line = data.splitlines()[0]
            method, path, _ = request_line.split(" ")
            parsed_path = urlparse(path)
            
            headers = self.parse_headers(data)
            
            if "Upgrade" in headers and headers["Upgrade"].lower() == "websocket":
                self.handle_websocket(client_socket, data, headers)
                return
            
            self.__verify_rest_method (
                data, 
                parsed_path
            )

            handler = self.routes.get(parsed_path.path)['handler']
            
            if handler:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        response_body = asyncio.run(handler()) 
                    else:
                        response_body = handler() 
                    status_line = "HTTP/1.1 200 OK\r\n"
                except Exception as e:
                    response_body = f"500 Internal Server Error: {e}"
                    status_line = "HTTP/1.1 500 Internal Server Error\r\n"
            else:
                response_body = "404 Not Found"
                status_line = "HTTP/1.1 404 Not Found\r\n"

            response = f"{status_line}Content-Type: text/plain\r\n\r\n{response_body}"
            client_socket.sendall(response.encode())
        
        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            client_socket.close()
            
    def __verify_rest_method (
        self,
        data,
        parsed_path
    ) -> None:
        
        operation_type = data.split('\n')[0].split('/')[0].strip(' ')
        if operation_type not in self.routes.get(parsed_path.path)['methods']:
            raise InvalidRestOperationType (
                self.routes.get(parsed_path.path)['methods'],
                operation_type,  
            )
                
    def websocket (
        self, 
        path,
    ) -> Callable[[Callable[..., None]], Callable[..., None]]:
        
        def wrapper (
            handler: Callable[..., None],
        ) -> Callable[..., None]:
            
            self.websockets[path] = handler
            return handler
        return wrapper
    
    def handle_websocket (
        self, 
        client_socket, 
        requests,
        headers
    ):
        
        sec_websocket_key = headers.get('Sec-WebSocket-Key')
        path = requests.split('\n')[0].split(' ')[1]
        
        if not sec_websocket_key or path not in self.websockets:
            client_socket.close()
            return
        
        accept_key = base64.b64encode(
            hashlib.sha1((sec_websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
        ).decode()
        
        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
        )
        client_socket.send(response.encode())
        
        self.websockets[path](client_socket)