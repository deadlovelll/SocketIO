from exceptions.base_exception.socketio_exception import SocketIOException

class DockerfileInvalidFileName(SocketIOException):
    
    def __init__ (
        self, 
        filename: str,
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Invalid dockerfile name '{filename}'.                                  #
#  All Dockerfiles should start with 'Dockerfile'.                        #
#  Please specify a valid file name.                                      #
{"#" * 75}
        """
        
        super().__init__(message)

class DockerfileInproperPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Invalid port number '{port}'.                                     #
#  Allowed port range: 0–65535.                                           #
#  Please specify a valid port within this range.                         #
{"#" * 75}
        """

        super().__init__(message)
        
class DockerfileForbieddenPortError(SocketIOException):
    
    def __init__ (
        self, 
        port: str
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Port '{port}' is reserved by the system.                            #
#  Please use a port number higher than 1024.                             #
#  System-reserved ports range: 0–1024.                                   #
{"#" * 75}
        """
        
        super().__init__(message)
        
class DockerfileNoSuchEntrypoint(SocketIOException):
    
    def __init__ (
        self, 
        filename: str,
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: The specified entrypoint file '{filename}' was not found.          #
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
    
    def __init__ (
        self,
    ) -> None:
        
        message = f"""
\n
{"#" * 75}
#  ERROR: Python file extension required.                                 #
#  The specified file must have a '.py' extension.                        #
#  Please ensure you are using a valid Python script.                     #
{"#" * 75}
        """
        
        super().__init__(message)
        
class DockerfileNoGRPCServiceEnabled(SocketIOException):
    
    def __init__(self) -> None:
        
        message = f"""
\n
{"#" * 77}
#  ERROR: No gRPC service is enabled.                                       #
#  A gRPC server must be properly configured and exposed in the Dockerfile. #
#  Please ensure that your application includes a running gRPC service.     #
{"#" * 77}
        """
        
        super().__init__(message)