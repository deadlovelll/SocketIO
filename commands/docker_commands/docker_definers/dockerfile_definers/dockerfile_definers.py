import textwrap

from SocketIO.commands.docker_commands.docker_definers.base_definer.base_definer import BaseDockerDefiner
from SocketIO.utils.os_detector.os_detector.os_detector import OSDetector

class PythonVesionDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        return f"python:{python_version}{'-alpine' if use_alpine else ''}"

class UserSecurityDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        use_nonroot_user: bool,
    ) -> str:
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
""") if use_nonroot_user else ""

class ExposedPortsDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        ports: list[int], 
        grpc_enabled: bool,
    ) -> str:
        
        ports = "\n".join(f"EXPOSE {port}" for port in ports)
        if grpc_enabled:
            ports += "\nEXPOSE 50051"
        return ports
    
class PoetryDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        poetry: bool, 
        in_env: bool,
    ) -> str:
        
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

class SystemDependenciesDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        install_system_deps: bool, 
        os_type: str,
    ) -> str:
        
        if not install_system_deps:
            return ""
        
        if not os_type:
            os_type = OSDetector().detect()
        
        depends_map = SystemDependenciesDefiner._get_os_map()
        
        return depends_map[os_type]
        
    @staticmethod
    def _get_os_map() -> dict:
        
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
            'macos': """\
RUN brew install coreutils
                """,
            'windows': """\
RUN choco install make mingw
                """,
        }
        
        depends_map['debian'] = depends_map['ubuntu']
        depends_map['rhel'] = depends_map['centos']
        
        return depends_map
