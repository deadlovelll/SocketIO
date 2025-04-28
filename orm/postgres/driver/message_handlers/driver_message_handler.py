"""
Postgres Driver Message Handler

This module defines the `PostgresDriverMessageHandler` class, which is responsible for handling 
various types of messages from a PostgreSQL server in a database driver context. Each type of 
message (e.g., authentication, error, query result) is processed by a corresponding handler 
method. These methods are mapped to specific message types using the `_message_type_map` dictionary.
"""

import struct

from typing import Any, Dict, Callable

from orm.postgres.driver.message_handlers.error.driver_error_message_handler import PostgresDriverErrorMessageHandler
from orm.postgres.driver.message_handlers.auth.driver_auth_message_handler import PostgresDriverAuthMessageHandler

from utils.static.privacy.privacy import privatemethod
from utils.static.privacy.protected_class import ProtectedClass


class PostgresDriverMessageHandler(ProtectedClass):
    
    """
    PostgresDriverMessageHandler

    A class responsible for handling different types of messages received from a PostgreSQL 
    database driver. This includes messages related to authentication, errors, query results, 
    and more. Each message type is processed by a specific handler method.

    Attributes:
    - _error_handler (PostgresDriverErrorMessageHandler): Handler for error messages.
    - _auth_handler (PostgresDriverAuthMessageHandler): Handler for authentication messages.
    - _message_type_map (Dict[bytes, Callable[[bytes], None]]): A mapping of message types to 
      their respective handler methods.
    - password (str): The password used for authentication.
    - user (str): The username used for authentication.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the PostgresDriverMessageHandler with the necessary handlers and 
        an empty message type map.

        The constructor sets up:
        - Error handler
        - Authentication handler
        - A dictionary mapping message types to handler methods
        """
        
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
        
        self._data_rows = []
        self._columns = []
        
    def cleanup (
        self,
    ) -> None:
        
        self._data_rows = []
        self._columns = []
        
    def get_data_rows (
        self,
    ) -> list[Any]:
        
        return self._data_rows
      
    @privatemethod  
    def _handle_auth (
        self,
        payload: bytes,
    ) -> None:
        
        """
        Handles authentication messages.

        Args:
        - payload (bytes): The message payload containing authentication data.

        This method delegates the authentication handling to the 
        PostgresDriverAuthMessageHandler.
        """
        
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
        
        """
        Handles error messages.

        Args:
        - payload (bytes): The message payload containing error data.

        This method delegates the error handling to the 
        PostgresDriverErrorMessageHandler.
        """
        
        self._error_handler.handle(payload)
        
    @privatemethod
    def _handle_ready_for_query (
        self,
        payload: bytes,
    ) -> str:
    
        """Handles 'Ready For Query' messages."""
        
        return 'break'
        
    
    @privatemethod
    def _handle_row_description (
        self,
        payload: bytes
    ) -> None:
        
        """Handles 'Row Description' messages."""
        
        column_count = struct.unpack('!H', payload[0:2])[0]
        offset = 2

        for _ in range(column_count):
            end = payload.find(b'\x00', offset)
            if end == -1:
                raise ValueError("Malformed RowDescription: no null terminator for column name")
            name = payload[offset:end].decode('utf-8')
            self._columns.append(name)
            offset = end + 1
            offset += 18
        print(self._columns)
    
    @privatemethod
    def _handle_data_row (
        self,
        payload: bytes
    ) -> None:
        
        """Handles 'Data Row' messages."""
        
        for column_data in payload:
            if column_data is None:
                self._data_rows.append(None)
            else:
                self._data_rows.append(column_data) 
        
        print(f"Data Row: {self._data_rows}")
    
    @privatemethod
    def _handle_command_complete (
        self,
        payload: bytes
    ):
        
        """Handles 'Command Complete' messages."""
        
        pass
    
    @privatemethod  
    def _handle_parameter_status (
        self,
        payload: bytes
    ):
        
        """Handles 'Parameter Status' messages."""
        
        pass
    
    @privatemethod
    def _handle_backend_key_data (
        self,
        payload: bytes
    ):
        
        """Handles 'Backend Key Data' messages."""
        
        pass
    
    @privatemethod
    def _handle_notice_response (
        self,
        payload: bytes
    ):
        
        """Handles 'Notice Response' messages."""
        
        pass
    
    @privatemethod
    def _handle_copy_in_response (
        self,
        payload: bytes
    ):
        
        """Handles 'Copy In Response' messages."""
        
        pass
    
    def handle (
        self,
        msg_type: bytes,
        payload: bytes,
        password: str,
        user: str,
    ) -> None:
        
        """
        Dispatches the message to the appropriate handler based on its type.

        Args:
        - msg_type (bytes): The type of the incoming message.
        - payload (bytes): The message payload.
        - password (str): The password for authentication.
        - user (str): The username for authentication.
        
        This method looks up the appropriate handler method in the `_message_type_map` 
        and calls it with the provided payload.
        """
        
        self.password = password
        self.user = user
        
        return self._message_type_map[msg_type](payload)