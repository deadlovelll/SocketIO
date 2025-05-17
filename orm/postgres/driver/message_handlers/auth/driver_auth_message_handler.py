"""
PostgreSQL Authentication Message Handler

This module defines the logic for processing authentication-related messages
from the PostgreSQL wire protocol. It handles multiple authentication methods,
such as plaintext and MD5-based authentication, and encapsulates logic to 
produce correct response payloads for each method.
"""

import hashlib
import struct

from typing import override

from exceptions.postgres_exceptions.postgres_exceptions import (
    SocketIOPostgresDriverAuthException,
)
from orm.postgres.driver.message_handlers.base.base_message_hander import (
    PostgresDriverBaseMessageHandler,
)
from utils.static.privacy.privacy import privatemethod


class PostgresDriverAuthMessageHandler (
    PostgresDriverBaseMessageHandler,
):
    
    """
    Handler for PostgreSQL authentication messages.

    This class interprets authentication requests sent by the PostgreSQL server and
    returns the appropriate responses, depending on the type of authentication required.

    Methods:
        - handle: Processes an authentication message and returns the appropriate response.
    """

    @privatemethod
    def _get_md5_encoded_password (
        self,
        user: str,
        password: str,
        salt: bytes,
    ) -> bytes:
        
        """
        Generates an MD5-encoded PostgreSQL password.

        Args:
            user (str): PostgreSQL username.
            password (str): PostgreSQL password.
            salt (bytes): 4-byte salt sent by the server.

        Returns:
            bytes: Encoded MD5 password with PostgreSQL-specific format.
        """
        
        step1 = hashlib.md5((password + user).encode()).hexdigest()
        step2 = hashlib.md5(step1.encode() + salt).hexdigest()
        return ('md5' + step2 + '\0').encode()

    @privatemethod
    def _get_encoded_password (
        self,
        password: str,
    ) -> bytes:
        
        """
        Encodes the password as a null-terminated UTF-8 byte string.

        Args:
            password (str): The password to encode.

        Returns:
            bytes: UTF-8 encoded password ending with a null byte.
        """
        
        return (password + '\0').encode()

    @override
    def handle(
        self,
        payload: bytes,
        password: str,
        user: str,
    ) -> str | bytes:
        
        """
        Handles an authentication request message from PostgreSQL.

        Args:
            payload (bytes): The raw message payload from the server.
            password (str): The client's password.
            user (str): The client's username.

        Returns:
            str | bytes: 'ready' if authentication is complete, or a response payload
            for the required authentication step.

        Raises:
            SocketIOPostgresDriverAuthException: If the server sends an unknown authentication method.
        """
        
        status_code = struct.unpack("!i", payload)[0]

        match status_code:
            case 0:
                return 'ready'
            case 3:
                return self._get_encoded_password(password)
            case 5:
                salt = payload[4:]
                return self._get_md5_encoded_password(user, password, salt)
            case _:
                raise SocketIOPostgresDriverAuthException()
