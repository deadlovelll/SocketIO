"""
This module defines a WebSocket handler that can manage WebSocket connections,
receive and send messages, and handle the handshake process for WebSocket communication.
"""

import socket
import base64
import hashlib
import struct

from utils.static.privacy.protected_class import ProtectedClass


class WebsocketHandler(ProtectedClass):
    
    """
    A handler for managing WebSocket connections, including performing the WebSocket handshake,
    receiving messages, and sending messages to clients.
    """
    
    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    """
    The magic string used in the WebSocket handshake to generate the accept key.
    """
    
    async def handle_websocket (
        self, 
        client_socket: socket.socket, 
        requests: str,
        headers: dict,
        websockets: dict,
    ) -> None:
        
        """
        Handles the WebSocket handshake by verifying the WebSocket key, generating the accept key,
        and upgrading the connection to a WebSocket connection.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.
            requests (str): The HTTP request string received from the client.
            headers (dict): The headers from the HTTP request.
            websockets (dict): A dictionary of active WebSocket connections, indexed by their paths.

        Returns:
            None
        """
        
        sec_websocket_key = headers.get('Sec-WebSocket-Key')
        path = requests.split('\n')[0].split(' ')[1]
        
        if not sec_websocket_key or path not in websockets:
            client_socket.close()
            return
        
        accept_key = base64.b64encode (
            hashlib.sha1((sec_websocket_key + self.MAGIC_STRING).encode()).digest()
        ).decode()
        
        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
        )
        client_socket.send(response.encode())
        
        websockets[path](client_socket)
    
    def receive_message (
        self, 
        client_socket: socket.socket,
    ) -> str | None:
        
        """
        Receives a WebSocket message from the client, decodes it, and returns the message content.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.

        Returns:
            str | None: The decoded message from the WebSocket, or None if no message is received or an error occurs.
        """
        
        try:
            data = client_socket.recv(2)
            if not data:
                return None
            
            opcode = data[0] & 0b00001111
            if opcode == 8:
                return None

            payload_length = data[1] & 127

            if payload_length == 126:
                data += client_socket.recv(2)
                payload_length = struct.unpack(">H", data[2:4])[0]
            elif payload_length == 127:
                data += client_socket.recv(8)
                payload_length = struct.unpack(">Q", data[2:10])[0]

            mask = client_socket.recv(4)
            encrypted_payload = client_socket.recv(payload_length)

            message = bytearray (
                encrypted_payload[i] ^ mask[i % 4] for i in range(payload_length)
            )
            return message.decode()
        except:
            return None

    def send_message (
        self, 
        client_socket: socket.socket, 
        message: str,
    ) -> None:
        
        """
        Sends a WebSocket message to the client, encoding it into a WebSocket frame.

        Args:
            client_socket (socket.socket): The socket representing the client's connection.
            message (str): The message to be sent to the client.

        Returns:
            None
        """
        
        encoded_message = message.encode()
        message_length = len(encoded_message)

        if message_length <= 125:
            frame = bytearray([129, message_length]) + encoded_message
        elif message_length <= 65535:
            frame = bytearray([129, 126]) + message_length.to_bytes(2, 'big') + encoded_message
        else:
            frame = bytearray([129, 127]) + message_length.to_bytes(8, 'big') + encoded_message

        client_socket.sendall(frame)