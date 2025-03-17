import textwrap

from commands.dockerfile_builder.dockerfile_validator.dockerfile_validator import DockerfileValidator

from commands.dockerfile_builder.dockerfile_creator.definers.exposed_ports_definer.exposed_ports_definer import ExposedPortsDefiner
from commands.dockerfile_builder.dockerfile_creator.definers.poetry_definer.poetry_definer import PoetryDefiner
from commands.dockerfile_builder.dockerfile_creator.definers.python_version_definer.python_version_definer import PythonVesionDefiner
from commands.dockerfile_builder.dockerfile_creator.definers.user_security_definer.user_security_definer import UserSecurityDefiner
from commands.dockerfile_builder.dockerfile_creator.definers.system_dependencies_definer.system_dependencies_definer import SystemDependenciesDefiner

class DockerfileFactory:

    @staticmethod
    def create (
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        poetry: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False,
        in_env: bool = False,
        os_type: str = None,
    ) -> str:
        
        python_version = PythonVesionDefiner.define_python_version (
            python_version, 
            use_alpine,
        )
        system_deps = SystemDependenciesDefiner.define_system_deps (
            install_system_deps, 
            os_type,
        )
        poetry = PoetryDefiner.define_poetry (
            poetry, 
            in_env,
        )
        user_security = UserSecurityDefiner.define_user_security (
            use_nonroot_user,
        )
        exposed_ports = ExposedPortsDefiner.define_exposed_ports (
            ports, 
            grpc_enabled,
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

        CMD ["python", "{entrypoint}"]
        """
        )

    @staticmethod
    def create_dockerfile (
        filename: str = "Dockerfile",
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        poetry: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False,
        in_env: bool = False,
        os_type: str = None
    ) -> None:
        
        DockerfileValidator.verify_dockerfile_args (
            python_version,
            use_alpine,
            ports,
            entrypoint,
            grpc_enabled,
        )
        
        with open(filename, "w") as f:
            f.write(DockerfileFactory.create (
                python_version, 
                use_alpine, 
                install_system_deps, 
                poetry, 
                ports, 
                entrypoint, 
                use_nonroot_user, 
                grpc_enabled,
                in_env,
                os_type,
            ))
        print(f"Dockerfile '{filename}' has been created.")