import asyncio
import socket
from urllib import urlparse

from handlers.http_handler.http_handler import HTTPHandler
from handlers.websocket_handler.websocket_handler import WebsocketHandler

from parsers.request_parser.request_parser import RequestParser

class RequestHandler:
    
    def __init__ (
        self,
    ) -> None:
        
        self.websocket_handler = WebsocketHandler()
        self.http_handler = HTTPHandler()
        
    def handle_request (
        self, 
        client_socket
    ):
        
        try:
            request_data = self.read_request(client_socket)
            if not request_data:
                return
            
            if not asyncio.run(self.__verify_host(client_socket)):
                client_socket.close()
                return

            request_line, headers = RequestParser.parse_request(request_data)
            method, path, _ = request_line.split(" ")
            parsed_path = urlparse(path)
            
            if self.is_websocket_request(headers):
                self.websocket_handler.handle_websocket (
                    client_socket, 
                    request_data, 
                    headers,
                )
            else:
                self.http_handler.handle_http_request (
                    request_data, 
                    path, 
                    parsed_path, 
                    client_socket,
                )
            
        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            client_socket.close()
            
    def read_request (
        self,
        client_socket: socket.socket,
    ) -> str:
        
        try:
            return client_socket.recv(1024).decode().strip()
        except Exception:
            return ""
    
    async def __verify_host (
        self, 
        client_socket,
    ):
        ip, port = client_socket.getpeername()
        
        return ip in self.allowed_hosts
    
    def is_websocket_request (
        self,
        headers,
    ) -> bool:
        
        return "Upgrade" in headers and headers["Upgrade"].lower() == "websocket"
        
    