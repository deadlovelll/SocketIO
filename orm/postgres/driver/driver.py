import socket
import struct


class PostgresDriver:
    
    def __init__ (
        self,
    ) -> None:
        
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.database_name = None
        
    def _buil_tartup_message(
        self,
    ) -> bytes:
        
        params = {
            'USER': self.user,
            'DATABASE': self.database_name,
        }
        
        payload = b''
        for k, v in params.items():
            payload += k.encode() + b'\x00' + v.encode() + b'\x00'
        payload += b'\x00'
        
        length = 4+4+len(payload)
        return struct.pack('!I', length) + struct.pack('!I', 0x00030000) + payload
    
    def _build_password_message(
        self,
    ) -> bytes:
        
        payload = self.password.encode() + b'\x00'
        length = 4 + len(payload)
        return b'p' + struct.pack('!I', length) + payload
    
    def _build_query_message(
        query: str,
    ) -> bytes:
        
        payload = query.encode() + b'\x00'
        length = 4 + len(payload)
        return b'Q' + struct.pack('!I', length) + payload
        
        
    