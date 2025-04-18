import os
import socket
import struct
import sys

from typing import Optional, Union

from orm.postgres.driver.driver_config import PostgresDriverConfig
from orm.postgres.driver.driver_message_builder import (
    PostgresDriverMessageBuilder,
)
from orm.postgres.driver.driver_message_handler.driver_message_handler import (
    PostgresDriverMessageHandler,
)


class PostgresDriver:
    
    def __init__ (
        self,
        driver_config: PostgresDriverConfig = PostgresDriverConfig()
    ) -> None:
        
        self.host = driver_config.host
        self.port = driver_config.port
        self.user = driver_config.user
        self.password = driver_config.password
        self.database_name = driver_config.database_name
        
        self.connection = None
                
        self.message_builder = PostgresDriverMessageBuilder()
        self.message_handler = PostgresDriverMessageHandler()
        
    def receive_message (
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
        
        self.connection.sendall(message)
    
    def establish_connection (
        self,
    ) -> None:
        
        self.connection = socket.create_connection((self.host, self.port))
        psql_message = self.message_builder.build_startup_message (
            self.user,
            self.database_name,
        )
        self.send_message(psql_message)
        self.consume_messages()
        
    def consume_messages(
        self,
    ) -> None:
        
        while True:
            msg_type, payload = self.receive_message()
            status_code = payload.split(b'\x00')[2].decode('utf-8')[1:]
            self.message_handler.handle(msg_type, payload)
        
# if __name__ == '__main__':
#     config = PostgresDriverConfig('localhost', 5432, 'my_user', 'user', 'my_secure_password')
#     d = PostgresDriver(config)
#     d.establish_connection()
        
    
        
    