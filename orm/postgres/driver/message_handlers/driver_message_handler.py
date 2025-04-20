from typing import Dict, Callable

from orm.postgres.driver.message_handlers.error.driver_error_message_handler import PostgresDriverErrorMessageHandler
from orm.postgres.driver.message_handlers.auth.driver_auth_message_handler import PostgresDriverAuthMessageHandler

from utils.static.privacy.privacy import privatemethod
from utils.static.privacy.protected_class import ProtectedClass

class PostgresDriverMessageHandler(ProtectedClass):
    
    def __init__ (
        self,
    ) -> None:
        
        self._error_handler = PostgresDriverErrorMessageHandler()
        self._auth_handler = PostgresDriverAuthMessageHandler()
        
        self._message_type_map: Dict[bytes, Callable[[bytes], None]] = {
            b'R': self._handle_auth,
            b'E': self._handle_error,
            b'Z': self._handle_ready_for_query,
            b'T': self._handle_row_description,
            b'D': self._handle_data_row,
            b'C': self._handle_command_complete,
            b'S': self._handle_parameter_status,
            b'K': self._handle_backend_key_data,
            b'N': self._handle_notice_response,
            b'G': self._handle_copy_in_response,
        }
        
        self.password = None
        self.user = None
      
    @privatemethod  
    def _handle_auth (
        self,
        payload: bytes,
    ) -> None:
        
        return self._auth_handler.handle (
            payload,
            self.password,
            self.user,
        )
    
    @privatemethod
    def _handle_error (
        self,
        payload: bytes,
    ) -> None:
        
        self._error_handler.handle(payload)
        
    @privatemethod
    def _handle_ready_for_query (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_row_description (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_data_row (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_command_complete (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod  
    def _handle_parameter_status (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_backend_key_data (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_notice_response (
        self,
        payload: bytes
    ):
        pass
    
    @privatemethod
    def _handle_copy_in_response (
        self,
        payload: bytes
    ):
        pass
    
    def handle (
        self,
        msg_type: bytes,
        payload: bytes,
        password: str,
        user: str,
    ) -> None:
        
        self.password = password
        self.user = user
        
        return self._message_type_map[msg_type](payload)