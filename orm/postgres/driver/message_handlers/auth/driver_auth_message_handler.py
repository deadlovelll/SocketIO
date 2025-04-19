import struct

from typing import override

from orm.postgres.driver.message_handlers.base.base_message_hander import (
    PostgresDriverBaseMessageHandler,
)


class PostgresDriverAuthMessageHandler (
    PostgresDriverBaseMessageHandler
):
    
    def __init__(
        self,
    ) -> None:
        
        super().__init__()
        
        self.status_code_map = {
            0: '',
            3: ''
        }
    
    @override
    def handle (
        self,
        payload: bytes,
    ) -> None:
        
        status_code = struct.unpack("!i", payload)[0]
        print(status_code)
        