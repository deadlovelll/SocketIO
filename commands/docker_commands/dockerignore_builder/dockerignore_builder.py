import textwrap

from commands.docker_commands.docker_definers.dockerignore_definers.dockerifnore_definers import (
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
    EnvFilesDefiner
)

class DockerignoreBuilder:
    
    @staticmethod
    def create_dockerignorefile_text (
        python_cache: bool,
        virtual_environment: bool,
        system_spec_files: bool,
        logs: bool,
        test_coverage: bool,
        git: bool,
        docker: bool,
        poetry,
        compiled_files: bool,
        documentation,
        env_files: bool,
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
            PythonCacheDefiner.define(python_cache),
            VenvDefiner.define(virtual_environment),
            SystemSpecsDefiner.define(system_spec_files),
            LogsDefine.define(logs),
            TestCoverageDefiner.define(test_coverage),
            GitAttributesDefiner.define(git),
            DockerFilesDefiner.define(docker),
            PoetryDefiner.define(poetry),
            CompiledFiledDefiner.define(compiled_files),
            DocumentationDefiner.define(documentation),
            EnvFilesDefiner.define(env_files),
        ]
        
        content = "\n\n".join(filter(None, sections))

        return textwrap.dedent(content).strip()
    
    @staticmethod
    def create_dockerignore_file (
        python_cache: bool = True,
        virtual_environment: bool = True,
        system_spec_files: bool = True,
        logs: bool = False,
        test_coverage: bool = True,
        git: bool = False,
        docker: bool = False,
        poetry: bool = False,
        compiled_files: bool = True,
        documentation: bool = True,
        env_files: bool = False,
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
        
        with open('.dockerignore', 'w') as f:
            f.write(DockerignoreBuilder.create_dockerignorefile_text (
                python_cache,
                virtual_environment,
                system_spec_files,
                logs,
                test_coverage,
                git,
                docker,
                poetry,
                compiled_files,
                documentation,
                env_files,
            ))
        print(f".dockerignore has been created.")