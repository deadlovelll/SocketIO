from exceptions.base_exception.socketio_exception import SocketIOException

class SocketIOStaticAccessException(SocketIOException):
    
    def __init__ (
        self, 
        attr_name: str,
    ) -> None:
        
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