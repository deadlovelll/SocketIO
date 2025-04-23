"""
This module defines a custom exception for handling invalid REST operation types
within the SocketIO framework.

Exceptions:
    - InvalidRestOperationType: Raised when a REST operation type does not match any of the expected values.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class InvalidRestOperationType(SocketIOException):
    
    """
    Exception raised when an invalid REST operation type is encountered.
    """

    def __init__ (
        self,
        expected: list[str],
        got: str,
    ) -> None:
        
        """
        Initializes the InvalidRestOperationType with a custom error message.

        Args:
            expected (list): A list of allowed REST operation types (e.g., ["GET", "POST"]).
            got (str): The invalid operation type that was received.

        Raises:
            SocketIOException: Inherited base exception.
        """
        
        message = f"""
{'#' * 80}
# ERROR: Invalid REST operation type, expected {' '.join(expected)}, got {got}.
#
# Please refer to the list of allowed operation types and choose a valid one.
{'#' * 80}
"""
        super().__init__(message.strip())
