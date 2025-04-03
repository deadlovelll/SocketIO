from exceptions.base_exception.socketio_exception import SocketIOException

class InvalidIsortVersion(SocketIOException):
    
    def __init__ (
        self, 
        version: str,
    ) -> None:
        
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
        super().__init__(message)
        
        
class InvalidIsortProfile(SocketIOException):
    
    def __init__ (
        self, 
        profile: str,
    ) -> None:
        
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

        super().__init__(profile)