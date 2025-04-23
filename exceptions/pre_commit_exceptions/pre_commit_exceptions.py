"""
This module defines a custom exception for errors related to invalid or non-existent
pre-commit-hooks versions.

Exceptions:
    - InvalidPreCommitHooksVersion: Raised when an invalid or non-existent version of 
      pre-commit-hooks is specified.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class InvalidPreCommitHooksVersion(SocketIOException):
    
    """
    Exception raised when an invalid or non-existent version of pre-commit-hooks is specified.

    This exception is raised if the version provided does not exist or is not valid.
    The user is directed to the official release page to check for available versions.
    """

    def __init__ (
        self, 
        version: str,
    ) -> None:
        
        """
        Initializes the InvalidPreCommitHooksVersion with a custom error message.

        Args:
            version (str): The invalid version of pre-commit-hooks that was specified.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
{'#' * 80}
# ERROR: The specified pre-commit-hooks version '{version}' is invalid or does not exist.
#
# You can check the list of valid versions here:
# https://github.com/pre-commit/pre-commit-hooks/releases
#
# If you're unsure about the version, omit it to use the latest available version.
{'#' * 80}
"""
        super().__init__(message)
