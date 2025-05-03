"""
Docker Definers Module

This module contains a set of classes responsible for generating
Dockerfile fragments related to Python versioning, system dependencies,
port exposure, user security, and dependency installation (via Poetry or pip).
"""

import textwrap
from commands.commands.docker.docker_definers.base_definer.base_definer import BaseDockerDefiner
from utils.os_detector.os_detector.os_detector import OSDetector


class PythonVesionDefiner(BaseDockerDefiner):
    
    """
    Defines the base Python image tag, optionally using an Alpine variant.
    """

    @staticmethod
    def define (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        """
        Returns the appropriate Python image tag.

        Args:
            python_version (str): Python version string, e.g., '3.11'.
            use_alpine (bool): Whether to use the Alpine-based image.

        Returns:
            str: Docker image tag.
        """
        
        return f"python:{python_version}{'-alpine' if use_alpine else ''}"


class UserSecurityDefiner(BaseDockerDefiner):
    
    """
    Defines a non-root user setup to improve container security.
    """

    @staticmethod
    def define (
        use_nonroot_user: bool,
    ) -> str:
        
        """
        Returns Docker commands to add and switch to a non-root user.

        Args:
            use_nonroot_user (bool): Whether to enable non-root user.

        Returns:
            str: Dockerfile content for user setup.
        """
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
        """) if use_nonroot_user else ""


class ExposedPortsDefiner(BaseDockerDefiner):
    
    """
    Defines ports to be exposed by the container.
    """

    @staticmethod
    def define (
        ports: list[int], 
        grpc_enabled: bool,
    ) -> str:
        
        """
        Returns EXPOSE directives.

        Args:
            ports (list[int]): List of ports to expose.
            grpc_enabled (bool): Whether to expose default gRPC port 50051.

        Returns:
            str: Dockerfile content for exposed ports.
        """
        
        result = "\n".join(f"EXPOSE {port}" for port in ports)
        if grpc_enabled:
            result += "\nEXPOSE 50051"
        return result
    
class PoetryDefiner(BaseDockerDefiner):
    
    """
    Defines commands to install Python dependencies using Poetry or pip.
    """

    @staticmethod
    def define (
        poetry: bool, 
        in_env: bool,
    ) -> str:
        
        """
        Returns Dockerfile content for dependency installation.

        Args:
            poetry (bool): Whether to use Poetry.
            in_env (bool): Whether to activate a virtualenv.

        Returns:
            str: Dockerfile content for installing dependencies.
        """
        
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
    
    """
    Defines system package installations based on the operating system.
    """

    @staticmethod
    def define (
        install_system_deps: bool, 
        os_type: str,
    ) -> str:
        
        """
        Returns Dockerfile content for system package installation.

        Args:
            install_system_deps (bool): Whether to install system dependencies.
            os_type (str): Type of OS (detected or provided).

        Returns:
            str: Dockerfile RUN commands for system packages.
        """
        
        if not install_system_deps:
            return ""
        
        if not os_type:
            os_type = OSDetector().detect()
        
        depends_map = SystemDependenciesDefiner._get_os_map()
        
        return depends_map[os_type]
        
    @staticmethod
    def _get_os_map() -> dict:
        
        """
        Returns a map of OS names to Dockerfile system dependency instructions.

        Returns:
            dict: Mapping of OS names to Docker RUN commands.
        """
        
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
