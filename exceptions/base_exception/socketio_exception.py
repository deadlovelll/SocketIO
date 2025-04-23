"""
This module defines custom exceptions for handling errors related to 
SocketIO operations. Specifically, it provides the `SocketIOException`, 
which serves as the base exception for all errors encountered in the 
context of SocketIO communications.

Exceptions:
    - SocketIOException: A custom exception for errors occurring during 
      SocketIO operations.
"""


class SocketIOException(Exception):
    
    """
    Base exception for all SocketIO-related errors.

    This exception serves as the base class for all exceptions that occur
    within the context of SocketIO operations. It can be used to catch
    any SocketIO-specific errors that might occur during socket communication.
    """
    
    def __init__ (
        self, 
        message: str,
    ) -> None:
        
        """
        Initializes the SocketIOException with a custom error message.

        Args:
            message (str): The error message describing the cause of the exception.
        """
        
        super().__init__(message)
