from typing import override

from orm.postgres.driver.sqlstate import SQLSTATE_MESSAGES
from orm.postgres.driver.driver_message_handler.base_message_hander import PostgresDriverBaseMessageHandler
from exceptions.postgres_exceptions.postgres_exceptions import SocketIOPostgresDriverException


class PostgresDriverErrorMessageHandler (
    PostgresDriverBaseMessageHandler
):
    
    @override
    def handle (
        self,
        payload: bytes,
    ) -> None:
        
        status_code = payload.split(b'\x00')[2].decode('utf-8')[1:]
        message = SQLSTATE_MESSAGES.get(status_code)
        raise SocketIOPostgresDriverException(status_code, message)