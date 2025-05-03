"""
DockerfileValidator module

This module provides the `DockerfileValidator` class, which is responsible for validating
input parameters used to generate a Dockerfile. It checks file name validity, port ranges,
Python image availability on Docker Hub, the existence and extension of the entrypoint file,
and gRPC-related environment conditions.
"""

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
    
    """
    A static class for validating Dockerfile generation parameters.
    """
    
    @staticmethod
    def verify_dockerfile_args (
        filename: str,
        python_version: str,
        use_alpine: bool,
        ports: list[int],
        entrypoint: str,
        grpc_enabled: bool,
    ) -> None:
        
        """
        Runs all individual validators for Dockerfile configuration arguments.

        Args:
            filename (str): Name of the Dockerfile.
            python_version (str): Python version tag.
            use_alpine (bool): Flag indicating if alpine image is used.
            ports (list[int]): Ports to be exposed.
            entrypoint (str): Application entrypoint file.
            grpc_enabled (bool): Flag for gRPC server integration.

        Raises:
            Dockerfile validation exceptions specific to each error.
        """
        
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
        
        """
        Ensures the Dockerfile name is valid.

        Args:
            filename (str): Dockerfile name.

        Raises:
            DockerfileInvalidFileName: If filename doesn't include 'Dockerfile'.
        """
        
        if 'Dockerfile' not in filename:
            raise DockerfileInvalidFileName(filename)
    
    @staticmethod
    def verify_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> None:
        
        """
        Validates the requested Python version against Docker Hub.

        Args:
            python_version (str): Python version string.
            use_alpine (bool): Whether the Alpine variant is requested.

        Raises:
            DockerfileNoSuchPythonVersionExists: If version tag doesn't exist on Docker Hub.
        """
        
        tag = f"{python_version}-alpine" if use_alpine else python_version
        url = f"https://hub.docker.com/v2/repositories/library/python/tags/{tag}/"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise DockerfileNoSuchPythonVersionExists(tag)
    
    @staticmethod
    def verify_port_validity (
        ports: list[int],
    ) -> None:
        
        """
        Ensures all specified ports are within allowed ranges.

        Args:
            ports (list[int]): List of port numbers.

        Raises:
            DockerfileForbieddenPortError: If a port is in reserved range (0–1023).
            DockerfileInproperPortError: If a port is invalid (>65535 or <0).
        """
        
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
        
        """
        Verifies that the entrypoint file exists and is a `.py` file.

        Args:
            entrypoint (str): Path to the entrypoint file.

        Raises:
            DockerfileNoSuchEntrypoint: If the file doesn't exist.
            DockerfilePyFileExtensionsRequired: If it's not a `.py` file.
        """
        
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
        
        """
        Ensures gRPC environment variable is set if gRPC is enabled.

        Args:
            grpc_enabled (bool): gRPC enablement flag.

        Raises:
            DockerfileNoGRPCServiceEnabled: If gRPC is enabled but environment variable is missing.
        """
        
        if grpc_enabled and not bool(os.environ.get('GRPC_SERVICE_ENABLED')):
            raise DockerfileNoGRPCServiceEnabled()