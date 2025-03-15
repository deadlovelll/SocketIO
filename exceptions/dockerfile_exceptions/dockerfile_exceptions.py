from exceptions.base_exception.socketio_exception import SocketIOException

class DockerfileInproperPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"Port {port} is not allowed. Ports range: 0–65535."
        super().__init__(message)
        
class DockerfileForbieddenPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"Port {port} is reserved by the system. Please use ports higher than 1024."
        super().__init__(message)
        
class DockerfileNoSuchEntrypoint(SocketIOException):
    
    def __init__ (
        self, 
        filename: str,
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: The specified entrypoint file '{filename}' was not found.         #
#  Please verify that the file exists and is correctly referenced.        #
{"#" * 75}
        """
        super().__init__(message)
        
class DockerfileNoSuchPythonVersionExists(SocketIOException):
    
    def __init__ (
        self, 
        python_version: str,
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: The specified Python version ({python_version})                              #
#  is not available on Docker Hub.                                        #
#  Please verify its existence using the link below:                      #
#  https://hub.docker.com/_/python                                        #
{"#" * 75}
        """
        
        super().__init__(message)
        
class DockerfilePyFileExtensionsRequired(SocketIOException):
    
    def __init__(self) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Python file extension required.                                 #
#  The specified file must have a '.py' extension.                        #
#  Please ensure you are using a valid Python script.                     #
{"#" * 75}
        """
        
        super().__init__(message)