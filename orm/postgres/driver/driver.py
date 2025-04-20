import os
import socket
import struct
import sys

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
    
    @privatemethod
    def _send_message (
        self,
        message: bytes,
    ) -> None:
        
        self.connection.sendall(message)
        
    @privatemethod
    def _build_query_message (
        self,
        query,
    ):
        query_bytes = query.encode('utf-8') + b'\x00'
        byte_length = len(query_bytes) + 4
        return b'Q' + struct.pack('!I', byte_length) + query_bytes
    
    @privatemethod
    def consume_messages (
        self,
    ) -> None:
        
        print(self.message_handler._message_type_map)
        
        while True:
            msg_type, payload = self._receive_message()
            result = self.message_handler.handle (
                msg_type, 
                payload, 
                self.password,
                self.user,
            )
            print(msg_type, payload)
            if result == 'ok':
                print('nice')
            elif isinstance(result, bytes):
                self.connection.sendall(result)
            elif result == 'abort':
                break
            
    def establish_connection (
        self,
    ) -> None:
        
        self.connection = socket.create_connection((self.host, self.port))
        psql_message = self.message_builder.build_startup_message (
            self.user,
            self.database_name,
            self.password,
        )
        self._send_message(psql_message)
        self.consume_messages()
        
# if __name__ == '__main__':
#     config = PostgresDriverConfig('localhost', 5432, 'my_user', 'my_secure_password', 'myapp_db')
#     d = PostgresDriver(config)
#     d.establish_connection()
        
    
        
    