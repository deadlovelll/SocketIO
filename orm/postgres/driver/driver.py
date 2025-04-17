from typing import Union

import socket

from orm.postgres.driver.driver_message_builder import PostgresDriverMessageBuilder


class PostgresDriver:
    
    def __init__ (
        self,
    ) -> None:
        
        self.message_builder = PostgresDriverMessageBuilder()
        
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.database_name = None
        
    def receive_message (
        self,
    ) -> Union[str, dict]:
        
        pass
    
    def send_message (
        self,
    ) -> None:
        
        pass
    
    def establish_connection (
        self,
    ) -> None:
        
        conn = socket.create_connection(self.host, self.port)
        psql_message = self.message_builder.build_startup_message (
            self.user,
            self.database_name,
        )
        conn.sendall(psql_message)
        
    