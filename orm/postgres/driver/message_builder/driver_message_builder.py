import struct

class PostgresDriverMessageBuilder:
    
    def build_startup_message (
        self,
        user: str,
        database_name: str,
        password: str,
    ) -> bytes:
        
        params = {
            'user': user,
            'database': database_name,
        }
        
        payload = b''
        for k, v in params.items():
            payload += k.encode() + b'\x00' + v.encode() + b'\x00'
        payload += b'\x00'
        
        length = 4+4+len(payload)
        return struct.pack('!I', length) + struct.pack('!I', 0x00030000) + payload
    
    def build_password_message (
        self,
        password: str,
    ) -> bytes:
        
        payload = password.encode() + b'\x00'
        length = 4 + len(payload)
        return b'p' + struct.pack('!I', length) + payload
    
    def build_query_message (
        query: str,
    ) -> bytes:
        
        payload = query.encode() + b'\x00'
        length = 4 + len(payload)
        return b'Q' + struct.pack('!I', length) + payload