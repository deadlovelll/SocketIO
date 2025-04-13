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
from commands.docker.dockerfile.dockerfile_config.dockerfile_config import (
    DockerfileConfig,
)
from interfaces.file_creator_interface.file_creator_interface import (
    FileCreator,
)


class DockerfileCreator(BaseCommand, FileCreator):
    
    def __init__(self, **options) -> None:
        super().__init__(**options)

    @staticmethod
    def create_file_text (
        config: DockerfileConfig = DockerfileConfig(),
    ) -> str:
        
        python_version = PythonVesionDefiner.define (
            config.python_version, 
            config.use_alpine,
        )
        system_deps = SystemDependenciesDefiner.define (
            config.install_system_deps, 
            config.os_type,
        )
        poetry = PoetryDefiner.define (
            config.poetry, 
            config.in_env,
        )
        user_security = UserSecurityDefiner.define (
            config.use_nonroot_user,
        )
        exposed_ports = ExposedPortsDefiner.define (
            config.ports, 
            config.grpc_enabled,
        )
        
        return textwrap.dedent (
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

    def create_file (
        self,
    ) -> None:
        
        config = DockerfileConfig(**self.options)
        text_content = self.create_file_text(config)
        
        with open(config.filename, 'w') as f:
            f.write(text_content)
            
        print(f"Dockerfile '{config.filename}' has been created.")
        
    @override
    def execute(self):
        self.create_file()
        
    