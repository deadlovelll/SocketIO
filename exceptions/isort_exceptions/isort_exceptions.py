"""
This module defines custom exceptions related to isort configuration issues
within the SocketIO framework.

Exceptions:
    - InvalidIsortVersion: Raised when an invalid or non-existent version of isort is specified.
    - InvalidIsortProfile: Raised when an unsupported isort profile is provided.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class InvalidIsortVersion(SocketIOException):
    
    """
    Exception raised when the specified isort version is invalid or does not exist.
    """

    def __init__ (
        self,
        version: str,
    ) -> None:
        
        """
        Initializes the InvalidIsortVersion with a formatted error message.

        Args:
            version (str): The invalid version of isort that was specified.

        Raises:
            SocketIOException: Inherited base exception.
        """
        
        message = f"""
{'#' * 80}
# ERROR: The specified isort version '{version}' is invalid or does not exist.
#
# You can check the list of valid versions here:
# https://github.com/PyCQA/isort/releases
#
# If you're unsure about the version, omit it to use the latest available version.
{'#' * 80}
"""
        super().__init__(message.strip())


class InvalidIsortProfile(SocketIOException):
    
    """
    Exception raised when an unsupported isort profile is provided.

    Attributes:
        profile (str): The invalid profile name provided by the user.
    """

    def __init__ (
        self,
        profile: str,
    ) -> None:
        
        """
        Initializes the InvalidIsortProfile with a formatted error message.

        Args:
            profile (str): The invalid or unsupported isort profile specified.

        Raises:
            SocketIOException: Inherited base exception.
        """
        
        message = f"""
{'#' * 80}
# ERROR: The specified isort profile '{profile}' is invalid or unsupported.
#
# Supported isort profiles include:
#   - black
#   - google
#   - pycharm
#   - pep8
#   - attrs
#
# Please choose one of the supported profiles or omit the profile option
# to use isort's default behavior.
{'#' * 80}
"""
        super().__init__(message.strip())
