import textwrap

from commands.docker_commands.docker_definers.dockerfile_definers.dockerfile_definers import (
    PythonVesionDefiner,
    SystemDependenciesDefiner,
    PoetryDefiner,
    UserSecurityDefiner,
    ExposedPortsDefiner,
)
from commands.docker_commands.dockerfile.dockerfile_validator.dockerfile_validator import DockerfileValidator
from interfaces.file_creator_interface.file_creator_interface import FileCreator

from commands.docker_commands.dockerfile.dockerfile_config.dockerfile_config import DockerfileConfig

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
        
        DockerfileValidator.verify_dockerfile_args (
            config.python_version,
            config.use_alpine,
            config.ports,
            config.entrypoint,
            config.grpc_enabled,
        )
        
        with open(config.filename, 'w') as f:
            f.write(DockerfileCreator.create (
                config
            ))
        print(f"Dockerfile '{config.filename}' has been created.")