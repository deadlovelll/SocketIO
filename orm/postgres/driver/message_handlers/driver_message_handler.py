from orm.postgres.driver.message_handlers.error.driver_error_message_handler import PostgresDriverErrorMessageHandler
from orm.postgres.driver.message_handlers.auth.driver_auth_message_handler import PostgresDriverAuthMessageHandler


class PostgresDriverMessageHandler:
    
    def __init__ (
        self,
    ) -> None:
        
        self._error_handler = PostgresDriverErrorMessageHandler()
        self._auth_handler = PostgresDriverAuthMessageHandler()
        
        self.message_type_map = {
            b'R': self._handle_auth,
            b'Z': 'cancel_requests',
            b'T': 'close_request',
            b'D': 'close_request',
            b'C': 'close_request',
            b'E': self._handle_error,
        }
    
    def _handle_error (
        self,
        payload: bytes,
    ) -> None:
        
        self._error_handler.handle(payload)
        
    def _handle_auth (
        self,
        payload: bytes,
    ) -> None:
        
        self._auth_handler.handle(payload)
    
    def handle (
        self,
        msg_type: bytes,
        payload: bytes,
    ) -> None:
        
        self.message_type_map[msg_type](payload)