import socket
import base64
import hashlib
import struct

class WebsocketHandler:
    
    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    
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
        
        self.websockets[path](client_socket)
        
    def receive_message (
        self, 
        client_socket: socket.socket,
    ) -> str:
        
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
        
        encoded_message = message.encode()
        message_length = len(encoded_message)

        if message_length <= 125:
            frame = bytearray([129, message_length]) + encoded_message
        elif message_length <= 65535:
            frame = bytearray([129, 126]) + message_length.to_bytes(2, 'big') + encoded_message
        else:
            frame = bytearray([129, 127]) + message_length.to_bytes(8, 'big') + encoded_message

        client_socket.sendall(frame)