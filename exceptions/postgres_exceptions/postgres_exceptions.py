"""
This module defines custom exceptions for handling PostgreSQL-related errors
within the SocketIO framework.

Exceptions:
    - SocketIOPostgresDriverException: Raised for general PostgreSQL driver errors with SQLSTATE codes.
    - SocketIOPostgresDriverAuthException: Raised for authentication errors with unknown PostgreSQL codes.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class SocketIOPostgresDriverException(SocketIOException):
    
    """
    Exception raised for PostgreSQL driver-level SQLSTATE errors.
    """

    def __init__ (
        self,
        sqlstate: str,
        message: str,
    ) -> None:
        
        """
        Initializes the SocketIOPostgresDriverException with a detailed message
        containing SQLSTATE and a reference link.

        Args:
            sqlstate (str): PostgreSQL SQLSTATE error code.
            message (str): Description of the SQL error.

        Raises:
            SocketIOException: Base class for all SocketIO-related exceptions.
        """
        
        formatted_message = f"""
{'#' * 80}
# ERROR: PostgreSQL error {sqlstate}: {message}.                               #
#                                                                              #
# See the full list of Postgres SQLSTATE codes here:                           #
# https://www.postgresql.org/docs/current/errcodes-appendix.html               #
#                                                                              #
# If you're not sure what this means, consult the above appendix.              #
{'#' * 80}
"""
        super().__init__(formatted_message.strip())


class SocketIOPostgresDriverAuthException(SocketIOException):
    
    """
    Exception raised for unknown PostgreSQL authentication failure codes.
    """

    def __init__ (
        self,
        unknown_code: str,
    ) -> None:
        
        """
        Initializes the SocketIOPostgresDriverAuthException with a helpful message
        indicating an unknown auth failure code and reference for further details.

        Args:
            unknown_code (str): The undocumented authentication code returned by PostgreSQL.

        Raises:
            SocketIOException: Base class for all SocketIO-related exceptions.
        """
        
        formatted_message = f"""
{'#' * 72}
# PostgreSQL authentication failed with unknown code: {unknown_code:<6}     #
#                                                                          #
# Refer to the full list of PostgreSQL auth codes:                         #
# → https://www.postgresql.org/docs/current/errcodes-appendix.html         #
#                                                                          #
# Tip: This might indicate protocol mismatch or server misconfiguration.  #
{'#' * 72}
"""
        super().__init__(formatted_message.strip())
