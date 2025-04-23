"""
This module defines a custom exception for handling errors when no Redis configuration is found
within the SocketIO framework.

Exceptions:
    - NoRedisConfiguredException: Raised when Redis configuration is not defined or not found.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class NoRedisConfiguredException(SocketIOException):
    
    """
    Exception raised when no Redis configuration is found.
    """

    def __init__(
        self,
        message: str = "No Redis configured. Are you sure that you defined Redis config with RedisConfig?"
    ) -> None:
        
        """
        Initializes the NoRedisConfiguredException with a custom error message.

        Args:
            message (str): The error message. Defaults to a generic message indicating missing Redis config.

        Raises:
            SocketIOException: Inherited base exception.
        """
        
        formatted_message = f"""
{'#' * 80}
# ERROR: {message}
#
# Please ensure that Redis is properly configured in your application
# using the RedisConfig class or equivalent configuration setup.
{'#' * 80}
"""
        super().__init__(formatted_message.strip())
