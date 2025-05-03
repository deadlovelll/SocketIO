"""
Dockerfile Configuration Module

Defines the `DockerfileConfig` dataclass used to configure Dockerfile generation
parameters for Python-based backend services.

This configuration class includes fields related to Python version,
Alpine-based images, system dependencies, Poetry, non-root user,
gRPC support, port exposure, and OS detection.

Validation is performed automatically on initialization via `DockerfileValidator`.
"""


from dataclasses import dataclass, field
from typing import List, Optional

from commands.commands.docker.dockerfile.dockerfile_validator.dockerfile_validator import DockerfileValidator


@dataclass
class DockerfileConfig:
    
    """
    Configuration holder for Dockerfile generation.

    Attributes:
        filename (str): Name of the Dockerfile. Defaults to 'Dockerfile'.
        python_version (str): Python version to use (e.g., '3.11' or 'latest').
        use_alpine (bool): Whether to use Alpine-based Python image. Defaults to False.
        install_system_deps (bool): Whether to install system dependencies. Defaults to True.
        poetry (bool): Whether to use Poetry for dependency management. Defaults to True.
        ports (List[int]): List of ports to expose. Defaults to [4000].
        entrypoint (str): Entrypoint script for the container. Defaults to 'main.py'.
        use_nonroot_user (bool): Whether to switch to a non-root user. Defaults to True.
        grpc_enabled (bool): Whether gRPC support is enabled. Defaults to False.
        in_env (bool): Whether to install dependencies inside a virtual environment. Defaults to False.
        os_type (Optional[str]): Override the detected operating system type. Defaults to None.
    """
    
    filename: str = 'Dockerfile'
    python_version: str = 'latest'
    use_alpine: bool = False
    install_system_deps: bool = True
    poetry: bool = True
    ports: List[int] = field(default_factory=lambda: [4000])
    entrypoint: str = 'main.py'
    use_nonroot_user: bool = True
    grpc_enabled: bool = False
    in_env: bool = False
    os_type: Optional[str] = None
    
    def __post_init__ (
        self,
    ) -> None:
        
        """
        Automatically validates key configuration fields after dataclass initialization
        using the `DockerfileValidator`.

        Raises:
            ValueError: If any of the provided configuration values are invalid.
        """
        
        DockerfileValidator.verify_dockerfile_args(
            self.filename,
            self.python_version,
            self.use_alpine,
            self.ports,
            self.entrypoint,
            self.grpc_enabled,
        )