"""
This module defines custom exceptions related to errors encountered 
during SocketIO operations, specifically dealing with access violations 
to protected class attributes.

Exceptions:
    - SocketIOStaticAccessException: Raised when there is an attempt to access
      a protected attribute outside its intended scope.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class SocketIOStaticAccessException(SocketIOException):
    
    """
    Exception raised when an attempt is made to access a protected attribute 
    from outside the class.

    Protected attributes, often starting with an underscore (`_`), are intended 
    for internal use only. If there is a need to access such an attribute, it is 
    recommended to provide a public interface or method.
    """

    def __init__ (
        self, 
        attr_name: str,
    ) -> None:
        
        """
        Initializes the SocketIOStaticAccessException with a custom error message.

        Args:
            attr_name (str): The name of the protected attribute that was 
                             accessed from outside the class.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
{'#' * 80}
#  ERROR: Attempt to access protected attribute '{attr_name}' from outside the class.         #
#                                                                                             #
#  Protected attributes (starting with '_') are meant for internal use only.                  #
#  If you need access, consider exposing a safe public interface or method.                   #
#                                                                                             #
{'#' * 80}
"""
        super().__init__(message.strip())
