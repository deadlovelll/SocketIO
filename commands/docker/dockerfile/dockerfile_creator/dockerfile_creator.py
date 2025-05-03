"""
DockerfileCreator module

This module provides the `DockerfileCreator` class which generates
a Dockerfile based on user-defined configuration using the `DockerfileConfig` dataclass.
It utilizes various definer classes to build different parts of the Dockerfile.
"""

import textwrap
from typing import override

from commands.base_command.base_command import BaseCommand
from commands.docker.docker_definers.dockerfile_definers.dockerfile_definers import (
    ExposedPortsDefiner,
    PoetryDefiner,
    PythonVesionDefiner,
    SystemDependenciesDefiner,
    UserSecurityDefiner,
)
from commands.docker.dockerfile.dockerfile_config.dockerfile_config import DockerfileConfig
from interfaces.file_creator_interface.file_creator_interface import FileCreator

from utils.static.privacy import (
    privatemethod,
    ProtectedClass,
)


class DockerfileCreator (
    BaseCommand, 
    FileCreator, 
    ProtectedClass,
):
    
    """
    Creates a Dockerfile using configurable options.

    Combines system dependencies, Python version selection, 
    Poetry setup, user permissions, and port exposure to 
    generate a structured multi-stage Dockerfile.
    """
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        """
        Initialize DockerfileCreator with provided options.
        
        Args:
            **options: Arbitrary keyword arguments for Dockerfile configuration.
        """
        
        super().__init__(**options)

    @privatemethod
    def _create_file_text (
        self,
        config: DockerfileConfig,
    ) -> str:
        
        """
        Generates Dockerfile content based on the configuration.

        Args:
            config (DockerfileConfig): Dockerfile configuration.

        Returns:
            str: The content of the Dockerfile.
        """
        
        python_version = PythonVesionDefiner.define(
            config.python_version, 
            config.use_alpine,
        )
        system_deps = SystemDependenciesDefiner.define(
            config.install_system_deps, 
            config.os_type,
        )
        poetry = PoetryDefiner.define(
            config.poetry, 
            config.in_env,
        )
        user_security = UserSecurityDefiner.define(
            config.use_nonroot_user,
        )
        exposed_ports = ExposedPortsDefiner.define(
            config.ports, 
            config.grpc_enabled,
        )
        
        return textwrap.dedent(
            f"""FROM {python_version} AS builder
            
WORKDIR /app

{system_deps}
{poetry}
COPY . .

FROM {python_version} AS final

WORKDIR /app
COPY --from=builder / /
{user_security}
{exposed_ports}

CMD ["python", "{config.entrypoint}"]
            """
        )

    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Writes the Dockerfile content to a file based on the given configuration.
        """
        
        config = DockerfileConfig(**self.options)
        text_content = self._create_file_text(config)

        with open(config.filename, 'w') as f:
            f.write(text_content)

        print(f"Dockerfile '{config.filename}' has been created.")
        
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Executes the Dockerfile creation command.
        """
        
        self._create_file()
