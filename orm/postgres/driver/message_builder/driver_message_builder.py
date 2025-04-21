"""
PostgreSQL Driver Message Builder

This module provides the `PostgresDriverMessageBuilder` class, responsible for constructing
low-level protocol-compliant byte messages used in communication with a PostgreSQL server.

It supports building:
- Startup message
- Password authentication message
- Query execution message

Each message follows the PostgreSQL frontend/backend protocol format.
"""

import struct

class PostgresDriverMessageBuilder:
    
    """
    Constructs PostgreSQL protocol messages for authentication and SQL query execution.

    Methods in this class return raw bytes to be sent over a socket connection
    to a PostgreSQL backend server.
    """
    
    def build_startup_message (
        self,
        user: str,
        database_name: str,
        password: str,
    ) -> bytes:
        
        """
        Constructs the startup message used to initiate a connection to PostgreSQL.

        Args:
            user (str): The PostgreSQL username.
            database_name (str): The name of the database to connect to.
            password (str): Unused in the message body, included for future compatibility.

        Returns:
            bytes: A properly formatted startup message.
        """
        
        params = {
            'user': user,
            'database': database_name,
        }
        
        payload = b''
        for k, v in params.items():
            payload += k.encode() + b'\x00' + v.encode() + b'\x00'
        payload += b'\x00'
        
        length = 4+4+len(payload)
        return struct.pack('!I', length) + struct.pack('!I', 0x00030000) + payload
    
    def build_password_message (
        self,
        password: str,
    ) -> bytes:
        
        """
        Constructs a password message in plain text format (cleartext password).

        Args:
            password (str): The user password to send.

        Returns:
            bytes: A message containing the password and its length prefix.
        """
        
        payload = password.encode() + b'\x00'
        length = 4 + len(payload)
        return b'p' + struct.pack('!I', length) + payload
    
    def build_query_message (
        query: str,
    ) -> bytes:
        
        """
        Constructs a query message used to send an SQL command to the PostgreSQL server.

        Args:
            query (str): The SQL query string to execute.

        Returns:
            bytes: A message containing the SQL query and its length prefix.
        """
        
        payload = query.encode() + b'\x00'
        length = 4 + len(payload)
        return b'Q' + struct.pack('!I', length) + payload