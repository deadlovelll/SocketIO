"""
Dockerignore Definers Module

This module contains classes that help define ignore rules for `.dockerignore` files.
Each class is responsible for a specific category such as Python cache, virtual environments,
logs, Docker configuration, Git metadata, documentation, etc.

All definers inherit from both `BaseDockerDefiner` and `BaseDockerignoreDefiner` and provide
a `define()` method that conditionally returns a string of ignore rules based on a boolean flag.
"""

from commands.docker.docker_definers.base_definer.base_definer import BaseDockerDefiner
from commands.docker.docker_definers.base_definer.base_dockerignore_definer import BaseDockerignoreDefiner


class PythonCacheDefiner(BaseDockerDefiner, BaseDockerignoreDefiner):
    
    """
    Defines patterns to ignore Python cache files.
    Includes `__pycache__/`, `.pyc`, `.pyo`, and `.pyd` files.
    """
    
    @classmethod
    def define (
        cls,
        python_cache: bool,
    ) -> str:
        
        """
        Generate ignore rules for Python cache files.

        Args:
            python_cache (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if python_cache:
            return super().add_ignorance (
                [
                    '__pycache__/',
                    '*.pyc',
                    '*.pyo',
                    '*.pyd',
                ]
            )
        return ''

class VenvDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore virtual environment files.
    Includes `venv/`, `.env/`, and `.venv/`.
    """
    
    @classmethod
    def define (
        cls,
        virtual_environment: bool,
    ) -> str:
        
        """
        Generate ignore rules for virtual environments.

        Args:
            virtual_environment (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if virtual_environment:
            return super().add_ignorance (
                [
                    'venv/',
                    '.env/',
                    '.venv/',
                ]
            )
        return ''
    
class SystemSpecsDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore system-specific files.
    Includes `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`, and `*.iml`.
    """
    
    @classmethod
    def define (
        cls,
        system_spec_files: bool,
    ) -> str:
        
        """
        Generate ignore rules for system-specific files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if system_spec_files:
            return super().add_ignorance (
                [
                    '.DS_Store',
                    'Thumbs.db',
                    '.idea/',
                    '.vscode/',
                    '*.iml',
                ]
            )
        return ''
    
class LogsDefine(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore logs and temporary files.
    Includes log files (`*.log`, `*.out`, `*.err`), temp files (`tmp/`), and swap files (`*.swp`, `*.swo`).
    """
    
    @classmethod
    def define (
        cls,
        logs: bool,
    ) -> str:
        
        """
        Generate ignore rules for logs and temp files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if logs:
            return super().add_ignorance (
                [
                    'logs/',
                    '*.log',
                    '*.out',
                    '*.err',
                    'tmp/',
                    '*.swp',
                    '*.swo',
                    'coverage/',
                    '*.cover',
                    '.pytest_cache/',
                ]
            )
            
class TestCoverageDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore test coverage files.
    Includes `tests/`, `coverage/`, `*.cover`, and `.pytest_cache/`.
    """
    
    @classmethod
    def define (
        cls,
        test_coverage: bool,
    ) -> str:
        
        """
        Generate ignore rules for test coverage files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if test_coverage:
            return super().add_ignorance (
                [
                    'tests/',
                    'coverage/',
                    '*.cover',
                    '*.pytest_cache/',
                ]
            )
        return ''
    

class GitAttributesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore Git-related files.
    Includes `.git/`, `.gitignore`, `.idea/`, `.vscode/`, and `*.iml`.
    """
    
    @classmethod
    def define (
        cls,
        git: bool,
    ) -> str:
        
        """
        Generate ignore rules for Git-related files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if git:
            return super().add_ignorance (
                [
                    '.git/',
                    '.gitignore',
                    '.idea/',
                    '.vscode/',
                    '*.iml',
                ]
            )
        return ''
    
    
class DockerFilesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore Docker-related files.
    Includes `.dockerignore`, `Dockerfile*`, and `docker-compose.yml`.
    """
    
    @classmethod
    def define (
        cls,
        docker: bool,
    ) -> str:
        
        """
        Generate ignore rules for Docker-related files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if docker:
            return super().add_ignorance (
                [
                    '.dockerignore',
                    'Dockerfile*',
                    'docker-compose.yml',
                ]
            )
        return ''

class PoetryDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore Poetry-related files.
    Includes `.poetry/`.
    """
    
    @classmethod
    def define (
        cls,
        poetry: bool,
    ) -> str:
        
        """
        Generate ignore rules for Poetry-related files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if poetry:
            return super().add_ignorance (
                [
                    '.poetry/',
                ]
            )
        return ''

class CompiledFiledDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore compiled files and build artifacts.
    Includes `dist/`, `build/`, and `*.egg-info/`.
    """
    
    @classmethod
    def define (
        cls,
        compiled_files: bool,
    ) -> str:
        
        """
        Generate ignore rules for compiled files and build artifacts.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if compiled_files:
            return super().add_ignorance (
                [
                    'dist/',
                    'build/',
                    '*.egg-info/',
                ]
            )
        return ''


class DocumentationDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore documentation files.
    Includes `docs/`, `*.md`, and `*.rst`.
    """
    
    @classmethod
    def define (
        cls,
        documentation: bool,
    ) -> str:
        
        """
        Generate ignore rules for documentation files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if documentation:
            return super().add_ignorance (
                [
                    'docs/',
                    '*.md',
                    '*.rst',
                ]
            )
        return ''
    

class EnvFilesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    """
    Defines patterns to ignore environment files.
    Includes `*.env`.
    """
    
    @classmethod
    def define (
        cls,
        env_files: bool,
    ) -> str:
        
        """
        Generate ignore rules for environment files.

        Args:
            logs (bool): Whether to include the rules.

        Returns:
            str: Dockerignore-compatible string of rules.
        """
        
        if env_files:
            return super().add_ignorance (
                [
                    '*.env',
                ]
            )
        return ''
