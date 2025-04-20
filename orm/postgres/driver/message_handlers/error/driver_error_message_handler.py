"""
Postgres Error Message Handler

This module defines a handler for PostgreSQL error messages
received via the low-level protocol. It parses the SQLSTATE code
from the payload and raises a structured exception.

Used in:
    - Low-level PostgreSQL client drivers
    - Binary protocol parsers
"""

from typing import override

from orm.postgres.driver.sqlstate.sqlstate import SQLSTATE_MESSAGES
from orm.postgres.driver.message_handlers.base.base_message_hander import (
    PostgresDriverBaseMessageHandler,
)
from exceptions.postgres_exceptions.postgres_exceptions import (
    SocketIOPostgresDriverException,
)


class PostgresDriverErrorMessageHandler (
    PostgresDriverBaseMessageHandler,
):
    
    """
    Handles PostgreSQL error messages (type 'E').

    This class extracts SQLSTATE error codes and raises descriptive
    exceptions based on known codes in the SQLSTATE_MESSAGES map.
    """

    @override
    def handle(
        self,
        payload: bytes,
    ) -> None:
        
        """
        Parse the error payload and raise an appropriate exception.

        Args:
            payload (bytes): Raw error message payload from PostgreSQL server.

        Raises:
            SocketIOPostgresDriverException: Raised with the SQLSTATE code and a description.
        """
        
        try:
            # SQLSTATE code is prefixed with a one-letter identifier, usually 'C'
            status_code = payload.split(b'\x00')[2].decode("utf-8")[1:]
            message = SQLSTATE_MESSAGES.get(status_code, "Unknown SQLSTATE error")
            raise SocketIOPostgresDriverException(status_code, message)
        
        except Exception as e:
            raise SocketIOPostgresDriverException (
                "UNKNOWN", f"Failed to parse error message: {e}"
            )