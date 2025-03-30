import textwrap

from commands.docker.docker_definers.dockerfile_definers.dockerfile_definers import (
    PythonVesionDefiner,
    SystemDependenciesDefiner,
    PoetryDefiner,
    UserSecurityDefiner,
    ExposedPortsDefiner,
)
from interfaces.file_creator_interface.file_creator_interface import FileCreator

from commands.docker.dockerfile.dockerfile_config.dockerfile_config import DockerfileConfig

class DockerfileCreator(FileCreator):

    @staticmethod
    def create_file_text (
        config: DockerfileConfig,
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

    @staticmethod
    def create_file (
        **options,
    ) -> None:
        
        config = DockerfileConfig(**options)
        
        with open(config.filename, 'w') as f:
            f.write(DockerfileCreator.create_file_text (
                config
            ))
        print(f"Dockerfile '{config.filename}' has been created.")