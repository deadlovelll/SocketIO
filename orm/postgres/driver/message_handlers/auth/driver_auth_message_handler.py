import struct

from typing import override

from SocketIO.orm.postgres.driver.sqlstate.sqlstate import SQLSTATE_MESSAGES
from orm.postgres.driver.driver_message_handler.base_message_hander import PostgresDriverBaseMessageHandler
from exceptions.postgres_exceptions.postgres_exceptions import SocketIOPostgresDriverException


class PostgresDriverAuthMessageHandler (
    PostgresDriverBaseMessageHandler
):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.status_code_map = {
            0: '',
        }
    
    @override
    def handle (
        self,
        payload: bytes,
    ) -> None:
        
        status_code = struct.unpack("!i", payload)[0]
        print(status_code)
        