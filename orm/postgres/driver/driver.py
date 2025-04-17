from typing import Union

import socket

from SocketIO.orm.postgres.driver.driver_message_builder import PostgresDriverMessageBuilder
from SocketIO.orm.postgres.driver.driver_config import PostgresDriverConfig

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
        
    def receive_message (
        self,
    ) -> Union[str, dict]:
        
        header = self.connection.recv(5)
        print(header)
    
    def send_message (
        self,
        message: bytes,
    ) -> None:
        
        self.connection.sendall(message)
    
    def establish_connection (
        self,
    ) -> None:
        
        self.connection = socket.create_connection(self.host, self.port)
        psql_message = self.message_builder.build_startup_message (
            self.user,
            self.database_name,
        )
        self.send_message(psql_message)
        
if __name__ == '__main__':
    d = PostgresDriver('localhost', 5432, 'my_user', 'user', 'my_secure_password')
    d.establish_connection()
        
    