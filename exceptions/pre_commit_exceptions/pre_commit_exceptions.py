from exceptions.base_exception.socketio_exception import SocketIOException

class InvalidPreCommitHooksVersion(SocketIOException):
    
    def __init__ (
        self, 
        version: str,
    ) -> None:
        
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