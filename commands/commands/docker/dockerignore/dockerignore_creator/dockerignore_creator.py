"""
DockerIgnoreCreator Module

This module defines the `DockerIgnoreCreator` class responsible for generating
a `.dockerignore` file for a project based on user-defined flags. Each flag
represents a category of files or directories to exclude from the Docker context.

The module supports various definer classes, each responsible for providing 
specific ignore patterns such as Python cache, virtual environments, logs,
Docker/Poetry configs, compiled files, and more.
"""

import textwrap

from typing import override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.commands.docker.docker_definers.dockerignore_definers.dockerifnore_definers import (
    PythonCacheDefiner,
    VenvDefiner,
    SystemSpecsDefiner,
    LogsDefine,
    TestCoverageDefiner,
    GitAttributesDefiner,
    DockerFilesDefiner,
    PoetryDefiner,
    CompiledFiledDefiner,
    DocumentationDefiner,
    EnvFilesDefiner,
)

from commands.commands.docker.dockerignore.dockerignore_config.dockerignore_config import DockerIgnoreConfig
from commands.base_command.base_command import BaseCommand

from utils.static.privacy import (
    privatemethod,
    ProtectedClass
)


class DockerIgnoreCreator (
    FileCreator, 
    BaseCommand,
    ProtectedClass,
):
    
    """
    DockerIgnoreCreator generates a `.dockerignore` file based on configuration flags.

    This class uses various definer classes to selectively include ignore patterns 
    for files and directories typically excluded from Docker build contexts. 
    It supports both static and dynamic configuration via the `DockerIgnoreConfig` dataclass.
    """
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        super().__init__(**options)
    
    @privatemethod
    def _create_file_text (
        self,
        config: DockerIgnoreConfig,
    ) -> str:
        
        """
        Generate the text content for a .dockerignore file based on specified flags.

        Each flag corresponds to a specific section of ignore patterns:
          - python_cache: Ignores Python cache directories and compiled files.
          - virtual_environment: Ignores virtual environment directories.
          - system_spec_files: Ignores system-specific or editor-specific files.
          - logs: Ignores log files and temporary files.
          - test_coverage: Ignores test directories, coverage reports, and caches.
          - git: Ignores Git-related files and directories.
          - docker: Ignores Docker-related configuration files.
          - poetry: Ignores Poetry-related files (if used for dependency management).
          - compiled_files: Ignores compiled or build artifact files.
          - documentation: Ignores documentation files (e.g., API docs, markdown files).
          - env_files: Ignores environment configuration files.

        Args:
            python_cache (bool): Include patterns for Python cache files.
            virtual_environment (bool): Include patterns for virtual environment directories.
            system_spec_files (bool): Include patterns for system-specific files.
            logs (bool): Include patterns for log and temporary files.
            test_coverage (bool): Include patterns for test files and coverage reports.
            git (bool): Include patterns for Git files.
            docker (bool): Include patterns for Docker configuration files.
            poetry (bool): Include patterns for Poetry dependency files.
            compiled_files (bool): Include patterns for build/compiled files.
            documentation (bool): Include patterns for documentation files.
            env_files (bool): Include patterns for environment files.

        Returns:
            str: A string containing the concatenated ignore patterns for the .dockerignore file.
        """
        
        sections = [
            PythonCacheDefiner.define(config.python_cache),
            VenvDefiner.define(config.virtual_environment),
            SystemSpecsDefiner.define(config.system_spec_files),
            LogsDefine.define(config.logs),
            TestCoverageDefiner.define(config.test_coverage),
            GitAttributesDefiner.define(config.git),
            DockerFilesDefiner.define(config.docker),
            PoetryDefiner.define(config.poetry),
            CompiledFiledDefiner.define(config.compiled_files),
            DocumentationDefiner.define(config.documentation),
            EnvFilesDefiner.define(config.env_files),
        ]
        
        content = "\n\n".join(filter(None, sections))

        return textwrap.dedent(content).strip()
    
    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Create a .dockerignore file in the current directory with the content generated
        from the specified flags.

        This method writes the output of `create_dockerignorefile_text` to a file named 
        `.dockerignore`, effectively generating the Docker ignore file for your project.

        Args:
            python_cache (bool, optional): Include ignore patterns for Python cache files.
                Defaults to True.
            virtual_environment (bool, optional): Include ignore patterns for virtual environments.
                Defaults to True.
            system_spec_files (bool, optional): Include ignore patterns for system-specific files.
                Defaults to True.
            logs (bool, optional): Include ignore patterns for logs and temporary files.
                Defaults to False.
            test_coverage (bool, optional): Include ignore patterns for test coverage and caches.
                Defaults to True.
            git (bool, optional): Include ignore patterns for Git files.
                Defaults to False.
            docker (bool, optional): Include ignore patterns for Docker-related files.
                Defaults to False.
            poetry (bool, optional): Include ignore patterns for Poetry files.
                Defaults to False.
            compiled_files (bool, optional): Include ignore patterns for compiled or build files.
                Defaults to True.
            documentation (bool, optional): Include ignore patterns for documentation files.
                Defaults to True.
            env_files (bool, optional): Include ignore patterns for environment files.
                Defaults to False.

        Returns:
            None: This method writes the .dockerignore file to disk.
        """
        
        config = DockerIgnoreConfig(*self.options)
        
        with open('.dockerignore', 'w') as f:
            f.write(self._create_file_text (
                config,
            ))
        print(f".dockerignore has been created.")
        
    @override
    def execute (
        self,
    ) -> None:
        
        self._create_file()