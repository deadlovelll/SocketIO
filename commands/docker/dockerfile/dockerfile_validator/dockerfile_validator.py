import os
import requests

from exceptions.dockerfile_exceptions.dockerfile_exceptions import (
    DockerfileInproperPortError, 
    DockerfileForbieddenPortError,
    DockerfileNoSuchEntrypoint,
    DockerfileNoSuchPythonVersionExists,
    DockerfilePyFileExtensionsRequired,
    DockerfileNoGRPCServiceEnabled,
    DockerfileInvalidFileName,
)

class DockerfileValidator:
    
    @staticmethod
    def verify_dockerfile_args (
        filename: str,
        python_version: str,
        use_alpine: bool,
        ports: list[int],
        entrypoint: str,
        grpc_enabled: bool,
    ) -> None:
        
        validators = {
            'verify_file_name': filename,
            'verify_python_version': (python_version, use_alpine),
            'verify_port_validity': ports,
            'verify_entrypoint_exists': entrypoint,
            'verify_grpc_enabled': grpc_enabled,
        }

        for method, args in validators.items():
            func = getattr(DockerfileValidator, method)
            func(*args if isinstance(args, tuple) else (args,))
        
    @staticmethod
    def verify_file_name (
        filename: str,
    ) -> None:
        
        if 'Dockerfile' not in filename:
            raise DockerfileInvalidFileName(filename)
    
    @staticmethod
    def verify_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> None:
        
        tag = f"{python_version}-alpine" if use_alpine else python_version
        url = f"https://hub.docker.com/v2/repositories/library/python/tags/{tag}/"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise DockerfileNoSuchPythonVersionExists(tag)
    
    @staticmethod
    def verify_port_validity (
        ports: list[int],
    ) -> None:
        
        forbidden_ports = list(range(0, 1024)) 
        dynamic_ports = list(range(49152, 65536))
        
        for port in ports:
            if port in forbidden_ports:
                raise DockerfileForbieddenPortError(port)
            elif port > 65535 or port < 0:
                raise DockerfileInproperPortError(port)
                
            elif port in dynamic_ports:
                print(f"Port {port} belongs to the dynamic range(49152–65535), conflicts may exist.")
                
    @staticmethod
    def verify_entrypoint_exists (
        entrypoint: str,
    ) -> None:
        
        is_file_exists = os.path.isfile(entrypoint)
        file_extension = entrypoint.split('.')[1]
        
        if not is_file_exists:
            raise DockerfileNoSuchEntrypoint(entrypoint)
        elif file_extension != 'py':
            raise DockerfilePyFileExtensionsRequired()
        
    @staticmethod
    def verify_grpc_enabled (
        grpc_enabled: bool,
    ) -> None:
        
        if grpc_enabled and not bool(os.environ.get('GRPC_SERVICE_ENABLED')):
            raise DockerfileNoGRPCServiceEnabled()