import socket
import struct

from typing import Optional, Union

from orm.postgres.driver.config.driver_config import PostgresDriverConfig
from orm.postgres.driver.message_builder.driver_message_builder import (
    PostgresDriverMessageBuilder,
)
from orm.postgres.driver.message_handlers.driver_message_handler import (
    PostgresDriverMessageHandler,
)
from utils.static.privacy.privacy import privatemethod


class PostgresDriver:
    
    def __init__ (
        self,
        driver_config: PostgresDriverConfig,
    ) -> None:
        
        self.host = driver_config.host
        self.port = driver_config.port
        self.user = driver_config.user
        self.password = driver_config.password
        self.database_name = driver_config.database_name
        
        self.connection = None
                
        self.message_builder = PostgresDriverMessageBuilder()
        self.message_handler = PostgresDriverMessageHandler()
      
    @privatemethod  
    def _receive_message (
        self,
    ) -> Union[Optional[str], Optional[dict]]:
        
        header = self.connection.recv(5)
        if len(header) < 5:
            return None, None
        msg_type = header[0:1]
        length = struct.unpack('!I', header[1:5])[0]-4
        payload = self.connection.recv(length)
        return msg_type, payload
    
    def send_message (
        self,
        message: bytes,
    ) -> None:
        
        self._ensure_connection()
        self.connection.sendall(message)
    
    def build_query_message (
        self,
        query,
    ):
        query_bytes = query.encode('utf-8') + b'\x00'
        byte_length = len(query_bytes) + 4
        return b'Q' + struct.pack('!I', byte_length) + query_bytes
    
    def consume_messages (
        self,
    ) -> None:
        
        while True:
            msg_type, payload = self._receive_message()
            print(msg_type, payload)
            if msg_type is None:
                break
            result = self.message_handler.handle (
                msg_type,
                payload,
                self.password,
                self.user,
            )

            if isinstance(result, bytes):
                self.connection.sendall(result)
            elif result == 'ready':
                rows = self.message_handler.get_data_rows()
                return rows
    
    @privatemethod       
    def _consume_until_ready (
        self,
    ) -> None:
        
        while True:
            msg_type, payload = self._receive_message()
            if msg_type is None:
                break
            
            result = self.message_handler.handle(
                msg_type,
                payload,
                self.password,
                self.user,
            )
            
            if isinstance(result, bytes):
                self.connection.sendall(result)
            elif result == 'break':  
                return
            
    def establish_connection (
        self,
    ) -> None:
        
        self.connection = socket.create_connection((self.host, self.port))
        psql_message = self.message_builder.build_startup_message(
            self.user,
            self.database_name,
            self.password,
        )
        self.send_message(psql_message)
        self._consume_until_ready()
        
    @privatemethod
    def _ensure_connection (
        self,
    ) -> None:
        
        if self.connection is None:
            self.establish_connection()
        
    def close_connection (
        self,
    ) -> None:
        
        if self.connection is not None:
            self.connection.close()
            self.connection = None
     
    def reconnect (
        self,
    ) -> None:
        
        self.close_connection()
        self.establish_connection()
            
    def __enter__ (
        self,
    ) -> None:
        
        self._ensure_connection()
        return self
    
    def __exit__ (
        self, exc_type, exc_val, exc_tb,
    ) -> None:
        
        self.close_connection()
        
    
        
    