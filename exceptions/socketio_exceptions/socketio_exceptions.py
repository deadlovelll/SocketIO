"""
This module defines custom exceptions for errors related to invalid or 
forbidden port numbers during SocketIO operations.

Exceptions:
    - SocketIOInproperPortError: Raised when an invalid port number is 
      specified (outside the valid port range).
    - SocketIOForbieddenPortError: Raised when a reserved (system) port 
      is used for SocketIO.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class SocketIOInproperPortError(SocketIOException):
    
    """
    Exception raised when an invalid port number is specified for SocketIO.

    This exception is raised if the port number provided is outside the valid
    port range (0–65535). It guides the user to choose a valid port number
    within the allowed range.
    """

    def __init__ (
        self, 
        port: str,
    ) -> None:
        
        """
        Initializes the SocketIOInproperPortError with a custom error message.

        Args:
            port (str): The invalid port number that was specified.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Invalid port number '{port}'.                             #
#  Allowed port range: 0–65535. Default SocketIO port is 4000             #
#  Please specify a valid port within this range.                         #
{"#" * 75}
        """
        super().__init__(message)


class SocketIOForbieddenPortError(SocketIOException):
    
    """
    Exception raised when a system-reserved (forbidden) port number is specified.

    This exception is raised when a port number from the system-reserved range
    (0–1024) is provided. The user is instructed to use a port number greater
    than 1024 to avoid conflicts with reserved ports.
    """

    def __init__ (
        self, 
        port: str,
    ) -> None:
        
        """
        Initializes the SocketIOForbieddenPortError with a custom error message.

        Args:
            port (str): The forbidden (system-reserved) port number that was specified.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
\n
{"#" * 80}
#  ERROR: Port '{port}' is reserved by the system.                               #
#  Please use a port number higher than 1024. Default SocketIO port is 4000    #
#  System-reserved ports range: 0–1024.                                        #
{"#" * 80}
        """
        super().__init__(message)
