"""
This module defines custom exceptions for handling errors related to 
SocketIO operations and specific errors related to the Black code formatter.

Exceptions:
    - InvalidBlackVersion: A specific exception raised when an invalid 
      version of the Black formatter is specified.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class InvalidBlackVersion(SocketIOException):
    
    """
    Exception raised when an invalid version of the Black formatter is specified.

    This exception is raised when the user provides an invalid or non-existent 
    version of the Black code formatter. The message provides guidance on how 
    to resolve the issue by checking the valid versions available.
    """

    def __init__ (
        self, 
        version: str,
    ) -> None:
        
        """
        Initializes the InvalidBlackVersion exception with a custom error message.

        Args:
            version (str): The invalid version of the Black formatter that caused the exception.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
{'#' * 80}
# ERROR: The specified black version '{version}' is invalid or does not exist.
#
# You can check the list of valid versions here:
# https://github.com/psf/black/releases
#
# If you're unsure about the version, omit it to use the latest available version.
{'#' * 80}
"""
        super().__init__(message)
