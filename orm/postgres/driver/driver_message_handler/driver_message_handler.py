from orm.postgres.driver.driver_message_handler.driver_error_message_handler import PostgresDriverErrorMessageHandler

class PostgresDriverMessageHandler:
    
    def __init__(
        self,
    ) -> None:
        
        self.error_handler = PostgresDriverErrorMessageHandler()
        
        self.message_type_map = {
            b'R': 'auth_request',
            b'Z': 'cancel_requests',
            b'T': 'close_request',
            b'D': 'close_request',
            b'C': 'close_request',
            b'E': self.handle_error,
        }
    
    def handle_error (
        self,
        payload: bytes,
    ) -> None:
        
        self.error_handler.handle(payload)
    
    def handle (
        self,
        msg_type: bytes,
        payload: bytes,
    ) -> None:
        
        self.message_type_map[msg_type](payload)