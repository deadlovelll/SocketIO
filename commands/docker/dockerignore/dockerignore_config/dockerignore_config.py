"""
DockerIgnoreConfig Module

This module defines the `DockerIgnoreConfig` dataclass, which is used to configure
what patterns should be ignored when generating a `.dockerignore` file.

The configuration enables selective exclusion of files and folders such as
Python caches, virtual environments, logs, system files, compiled artifacts,
documentation, and more.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DockerIgnoreConfig:
    
    """
    Configuration dataclass for controlling contents of a generated `.dockerignore` file.
    
    Each flag indicates whether a specific category of files should be ignored.
    """
    
    python_cache: bool = True
    """Ignore Python bytecode files and `__pycache__` folders."""

    virtual_environment: bool = True
    """Ignore virtual environment folders like `venv/`, `.env/`, `.venv/`."""

    system_spec_files: bool = True
    """Ignore system-specific files such as `.DS_Store`, `Thumbs.db`, and IDE configs."""

    logs: Optional[bool] = False
    """Ignore log files and temporary output (e.g. `*.log`, `tmp/`)."""

    test_coverage: bool = True
    """Ignore files related to test coverage, such as `.pytest_cache/`, `*.cover`, `coverage/`."""

    git: Optional[bool] = False
    """Ignore Git-related files and folders like `.git/`, `.gitignore`."""

    docker: Optional[bool] = False
    """Ignore Docker-specific files like `Dockerfile`, `.dockerignore`, and docker-compose files."""

    poetry: Optional[bool] = False
    """Ignore Poetry-specific folders such as `.poetry/`."""

    compiled_files: bool = True
    """Ignore build artifacts like `dist/`, `build/`, and `*.egg-info/`."""

    documentation: bool = True
    """Ignore documentation files like `.md`, `.rst`, and `docs/`."""

    env_files: Optional[bool] = False
    """Ignore environment files such as `.env`, `.env.*`."""
