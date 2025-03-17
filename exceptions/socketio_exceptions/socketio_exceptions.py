from exceptions.base_exception.socketio_exception import SocketIOException

class SocketIOInproperPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Invalid port number '{port}'.                             #
#  Allowed port range: 0–65535. Default SocketIO port is 4000             #
#  Please specify a valid port within this range.                         #
{"#" * 75}
        """

        super().__init__(message)
        
class SocketIOForbieddenPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"""
\n
{"#" * 80}
#  ERROR: Port '{port}' is reserved by the system.                               #
#  Please use a port number higher than 1024. Default SocketIO port is 4000    #
#  System-reserved ports range: 0–1024.                                        #
{"#" * 80}
        """
        
        super().__init__(message)