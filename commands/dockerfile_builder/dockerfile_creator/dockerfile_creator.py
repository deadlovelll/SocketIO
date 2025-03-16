import textwrap
import platform
import os

from commands.dockerfile_builder.dockerfile_validator.dockerfile_validator import DockerfileValidator

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
        
        python_version = DockerfileFactory._define_python_version(python_version, use_alpine)
        system_deps = DockerfileFactory._define_system_deps(install_system_deps, os_type)
        poetry = DockerfileFactory._define_poetry(poetry, in_env)
        user_security = DockerfileFactory._define_user_security(use_nonroot_user)
        exposed_ports = DockerfileFactory._define_exposed_ports(ports, grpc_enabled)
        
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
    def _define_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        return f"python:{python_version}{'-alpine' if use_alpine else ''}"

    @staticmethod
    def _define_exposed_ports (
        ports: list[int], 
        grpc_enabled: bool,
    ) -> str:
        
        ports = "\n".join(f"EXPOSE {port}" for port in ports)
        if grpc_enabled:
            ports += "\nEXPOSE 50051"
        return ports

    @staticmethod
    def _define_system_deps (
        install_system_deps: bool, 
        os_type: str,
    ) -> str:
        
        if not install_system_deps:
            return ""
        
        if not os_type:
            os_type = platform.platform()
            
        print(os_type)
        
        depends_map = DockerfileFactory.get_os_map()
        
        return 
        # else:
        #     raise ValueError(f"Unsupported OS type: {os_type}")
        
    @staticmethod
    def define_user_os():
        pass
        
    @staticmethod
    def get_os_map() -> dict:
        
        depends_map = {
            'ubuntu': """\
                RUN apt-get update && \\
                    apt-get install -y --no-install-recommends \\
                    build-essential && \\
                    rm -rf /var/lib/apt/lists/*
                """,
            'alpine': """\
                RUN apk add --no-cache \\
                    build-base
                """,
            'centos': """\
                RUN yum groupinstall -y "Development Tools" && \\
                    yum clean all
                """,
            'arch': """\
                RUN pacman -Syu --noconfirm base-devel
                """,
            'darwin': """\
                RUN brew install coreutils
                """,
            'windows': """\
                RUN choco install make mingw
                """,
        }
        
        depends_map['debian'] = depends_map['ubuntu']
        depends_map['rhel'] = depends_map['centos']
        
        return depends_map

    @staticmethod
    def _define_poetry(poetry: bool, in_env: bool) -> str:
        env_setup = """\
RUN python -m venv /venv && \\
    . /venv/bin/activate
""" if in_env else ""

        if poetry:
            return f"""\
{env_setup}COPY pyproject.toml poetry.lock ./
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel && \\
    pip install poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --no-dev --no-interaction --no-ansi --no-root
"""
        else:
            return f"""{env_setup}COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel && \\
    pip install -r requirements.txt
    """

    @staticmethod
    def _define_user_security (
        use_nonroot_user: bool,
    ) -> str:
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
""") if use_nonroot_user else ""

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