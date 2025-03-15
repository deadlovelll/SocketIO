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
        
        message = f"Entrypoint {filename} does not exist. Please verify the file existance."
        super().__init__(message)
        
class DockerfileNoSuchPythonVersionExists(SocketIOException):
    
    def __init__ (
        self, 
        python_version: str,
    ) -> None:
        
        message = f"""
        Python version {python_version} does not exist in Dockerhub. 
        You can verify it by the link below https://hub.docker.com/_/python.
        """
        
        super().__init__(message)