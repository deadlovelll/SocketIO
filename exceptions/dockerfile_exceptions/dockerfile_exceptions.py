"""
This module defines custom exceptions for handling Dockerfile-related errors
within the SocketIO framework.

Exceptions:
    - DockerfileInvalidFileName: Raised when the specified Dockerfile has an invalid name.
    - DockerfileInproperPortError: Raised when an invalid port number is provided in the Dockerfile.
    - DockerfileForbieddenPortError: Raised when a system-reserved port is used in the Dockerfile.
    - DockerfileNoSuchEntrypoint: Raised when the entrypoint file in the Dockerfile is not found.
    - DockerfileNoSuchPythonVersionExists: Raised when the specified Python version is not available on Docker Hub.
    - DockerfilePyFileExtensionsRequired: Raised when a Python file does not have the required `.py` extension.
    - DockerfileNoGRPCServiceEnabled: Raised when no gRPC service is enabled in the Dockerfile.
"""

from exceptions.base_exception.socketio_exception import SocketIOException


class DockerfileInvalidFileName(SocketIOException):
    
    """
    Exception raised when the specified Dockerfile has an invalid name.
    """

    def __init__ (
        self, 
        filename: str,
    ) -> None:
        
        """
        Initializes the DockerfileInvalidFileName with a custom error message.

        Args:
            filename (str): The invalid Dockerfile name.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
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
    
    """
    Exception raised when an invalid port number is provided in the Dockerfile.
    """

    def __init__ (
        self, 
        port: str,
    ) -> None:
        
        """
        Initializes the DockerfileInproperPortError with a custom error message.

        Args:
            port (str): The invalid port number.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
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
    
    """
    Exception raised when a system-reserved port is used in the Dockerfile.
    """

    def __init__ (
        self, 
        port: str,
    ) -> None:
        
        """
        Initializes the DockerfileForbieddenPortError with a custom error message.

        Args:
            port (str): The system-reserved port number.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
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
    
    """
    Exception raised when the specified entrypoint file in the Dockerfile is not found.
    """

    def __init__ (
        self, 
        filename: str,
    ) -> None:
        
        """
        Initializes the DockerfileNoSuchEntrypoint with a custom error message.

        Args:
            filename (str): The entrypoint file name that was not found.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
\n
{"#" * 75}
#  ERROR: The specified entrypoint file '{filename}' was not found.          #
#  Please verify that the file exists and is correctly referenced.        #
{"#" * 75}
        """
        
        super().__init__(message)


class DockerfileNoSuchPythonVersionExists(SocketIOException):
    
    """
    Exception raised when the specified Python version is not available on Docker Hub.
    """

    def __init__ (
        self, 
        python_version: str,
    ) -> None:
        
        """
        Initializes the DockerfileNoSuchPythonVersionExists with a custom error message.

        Args:
            python_version (str): The Python version that was not found.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
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
    
    """
    Exception raised when a Python file does not have the required `.py` extension.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the DockerfilePyFileExtensionsRequired with a custom error message.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
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
    
    """
    Exception raised when no gRPC service is enabled in the Dockerfile.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the DockerfileNoGRPCServiceEnabled with a custom error message.

        Raises:
            SocketIOException: Inherits from the base `SocketIOException` class.
        """
        
        message = f"""
\n
{"#" * 77}
#  ERROR: No gRPC service is enabled.                                       #
#  A gRPC server must be properly configured and exposed in the Dockerfile. #
#  Please ensure that your application includes a running gRPC service.     #
{"#" * 77}
        """
        
        super().__init__(message)