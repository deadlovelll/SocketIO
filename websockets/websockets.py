import socket
import hashlib
import base64
import threading

class WebSocketServer:
    
    def __init__ (
        self,
        host,
        port
    ) -> None:
        
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        
    def start(self):
        pass
    
    def handler_client(self):
        pass
    
    def handshake(self):
        pass
    
    def receive_message(self):
        pass
    
    def send_message(self):
        pass
    
    def broadcast(self):
        pass
    
    