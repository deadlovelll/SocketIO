"""
This module contains various `GitIgnore*Definer` classes that extend 
`BaseGitIgnoreDefiner` and define specific sections of a `.gitignore` file
based on typical development environments and concerns.

Each class is responsible for generating a string section for the `.gitignore` 
file, based on a corresponding boolean flag.

Available definers:
    - GitIgnoreByteCodeDefiner
    - GitIgnoreVenvDefiner
    - GitIgnoreLogsDefiner
    - GitIgnorePackagingDefiner
    - GitIgnoreOsSpecificFilesDefiner
    - GitIgnoreIDEFilesDefiner
    - GitIgnoreCoverageDefiner
    - GitIgnoreCachesDefiner
    - GitIgnoreDockerDefiner
    - GitIgnoreGRPCDefiner
    - GitIgnoreJupyterCopyBookDefiner
    - GitIgnoreTestingDefiner
    - GitIgnoreSecurityDefiner
"""

from commands.commands.git.base_definers.base_gitignore_definer import BaseGitIgnoreDefiner


class GitIgnoreByteCodeDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for Python bytecode files to be ignored in .gitignore.

    Adds common patterns for compiled Python files such as `.pyc`, `.pyo`, and 
    the `__pycache__/` directory.

    Inherits from:
        BaseGitIgnoreDefiner
    """
    
    def define (
        self,
        bytecode_files: bool,
    ) -> str:
        
        """
        Generate .gitignore section for bytecode files.

        Args:
            bytecode_files (bool): Flag to determine whether to include this section.

        Returns:
            str: The bytecode ignore patterns or an empty string if disabled.
        """
        
        if bytecode_files:
            return super().add_ignorance (
                [
                    '__pycache__/',
                    '*.py[cod]',
                    '*$py.class',
                    '*.pyc',
                    '*.pyd',
                    '*.pyo',
                ]
            )
        return ''


class GitIgnoreVenvDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for virtual environment directories to be ignored in .gitignore.

    This class defines common patterns used for virtual environment folders
    created by tools like venv, virtualenv, and pipenv.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        venv: bool,
    ) -> str:
        
        """
        Generate .gitignore section for virtual environment directories.

        Args:
            venv (bool): Whether to include virtual environment paths in the .gitignore file.

        Returns:
            str: The formatted ignore section for virtual environment directories, 
                or an empty string if not enabled.
        """
        
        if venv:
            return super().add_ignorance (
                [
                    'venv/',
                    'env/',
                    '.venv/',
                    'ENV/',
                ]
            )
        return ''
            
    
class GitIgnoreLogsDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for log and database-related files to be ignored in .gitignore.

    This class targets common output files like logs, SQLite databases, and SQL dumps,
    which are typically not tracked in source control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        logs: bool,
    ) -> str:
        
        """
        Generate .gitignore section for log and database files.

        Args:
            logs (bool): Whether to include log and local database files in the .gitignore file.

        Returns:
            str: The formatted ignore section for log/database files, 
                or an empty string if not enabled.
        """
        
        if logs:
            return super().add_ignorance (
                [
                    '*.log',
                    '*.sqlite3',
                    '*.db',
                    '*.sql',
                ]
            )
        return ''
    
    
class GitIgnorePackagingDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for packaging-related files to be ignored in .gitignore.

    This class defines the common files and directories that should be ignored
    when working with Python packaging, including build artifacts and metadata.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        packaging: bool,
    ) -> str:
        
        """
        Generate .gitignore section for packaging-related files.

        Args:
            packaging (bool): Whether to include packaging-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for packaging files, 
                or an empty string if not enabled.
        """
        
        if packaging:
            return super().add_ignorance (
                [
                    'build/',
                    'dist/',
                    '*.egg-info/',
                    'pip-wheel-metadata/',
                ]
            )
        return ''
    
    
class GitIgnoreOsSpecificFilesDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for operating system-specific files to be ignored in .gitignore.

    This class defines common files that operating systems like macOS and Windows
    generate, which typically should not be tracked in version control systems.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        os_specific: bool,
    ) -> str:
        
        """
        Generate .gitignore section for OS-specific files.

        Args:
            os_specific (bool): Whether to include OS-specific files in the .gitignore file.

        Returns:
            str: The formatted ignore section for OS-specific files, 
                or an empty string if not enabled.
        """
        
        if os_specific:
            return super().add_ignorance (
                [
                    '.DS_Store',
                    'Thumbs.db',
                ]
            )
        return ''
    
    
class GitIgnoreIDEFilesDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for IDE-related files to be ignored in .gitignore.

    This class defines common files and directories that are typically generated
    by Integrated Development Environments (IDEs) like JetBrains and Visual Studio Code,
    which should not be included in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        ide_files: bool,
    ) -> str:
        
        """
        Generate .gitignore section for IDE-related files.

        Args:
            ide_files (bool): Whether to include IDE-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for IDE files, 
                or an empty string if not enabled.
        """
        
        if ide_files:
            return super().add_ignorance (
                [
                    '.idea/',
                    '.vscode/',
                    '*.swp',
                    '*.swo',
                    '*.swn',
                ]
            )
        return ''
    
    
class GitIgnoreCoverageDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for coverage-related files to be ignored in .gitignore.

    This class defines common files and directories related to test coverage
    tools (such as pytest and coverage.py), which should not be tracked in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        coverage: bool,
    ) -> str:
        
        """
        Generate .gitignore section for coverage-related files.

        Args:
            coverage (bool): Whether to include coverage-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for coverage files, 
                or an empty string if not enabled.
        """
        
        if coverage:
            return super().add_ignorance (
                [
                    '.coverage',
                    'htmlcov/',
                    'coverage.xml',
                ]
            )
        return ''
            
            
class GitIgnoreCachesDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for cache-related files to be ignored in .gitignore.

    This class defines common cache directories and files generated by tools
    like pytest and mypy that should be ignored in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        caches: bool,
    ) -> str:
        
        """
        Generate .gitignore section for cache-related files.

        Args:
            caches (bool): Whether to include cache-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for cache files, 
                or an empty string if not enabled.
        """
        
        if caches:
            return super().add_ignorance (
                [
                    '.cache/',
                    '*.mypy_cache/',
                    '.pytest_cache/',
                ]
            )
        return ''
    
    
class GitIgnoreDockerDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for Docker-related files to be ignored in .gitignore.

    This class defines common Docker-related files and directories,
    such as Docker Compose override files and Dockerfile extensions,
    which should not be included in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        docker: bool,
    ) -> str:
        
        """
        Generate .gitignore section for Docker-related files.

        Args:
            docker (bool): Whether to include Docker-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for Docker files, 
                or an empty string if not enabled.
        """
        
        if docker:
            return super().add_ignorance (
                [
                    'docker-compose.override.yml',
                    '*.dockerfile',
                    '*.tar',    
                ]
            )
        return ''
    
    
class GitIgnoreGRPCDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for gRPC-related files to be ignored in .gitignore.

    This class defines files generated by gRPC tools, such as Python gRPC
    stub files, which should not be tracked in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        grpc: bool,
    ) -> str:
        
        """
        Generate .gitignore section for gRPC-related files.

        Args:
            grpc (bool): Whether to include gRPC-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for gRPC files, 
                or an empty string if not enabled.
        """
        
        if grpc:
            return super().add_ignorance (
                [
                    '*_pb2.py',
                    '*_pb2_grpc.py',
                ]
            )
        return ''
    
    
class GitIgnoreJupyterCopyBookDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for Jupyter notebook checkpoint files to be ignored in .gitignore.

    This class adds rules to ignore directories containing Jupyter notebook
    checkpoint files, which should not be included in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        jupyter_cp: bool,
    ) -> str:
        
        """
        Generate .gitignore section for Jupyter notebook checkpoint files.

        Args:
            jupyter_cp (bool): Whether to include Jupyter checkpoint files in the .gitignore file.

        Returns:
            str: The formatted ignore section for Jupyter checkpoint files,
                or an empty string if not enabled.
        """
        
        if jupyter_cp:
            return super().add_ignorance (
                [
                    '.ipynb_checkpoints/',
                ]
            )
        return ''
    

class GitIgnoreTestingDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for test-related files to be ignored in .gitignore.

    This class defines common directories and files related to testing, 
    such as test reports and `__pycache__` folders, that should be ignored in version control.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        testing: bool,
    ) -> str:
        
        """
        Generate .gitignore section for test-related files.

        Args:
            testing (bool): Whether to include test-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for test files, 
                or an empty string if not enabled.
        """
        
        if testing:
            return super().add_ignorance (
                [
                    'test-reports/',
                    'tests/__pycache__/',
                ]
            )
    
    
class GitIgnoreSecurityDefiner(BaseGitIgnoreDefiner):
    
    """
    Definer for security-related files to be ignored in .gitignore.

    This class defines sensitive configuration and secrets files, such as `.env` files and 
    `secrets.json`, which should not be tracked in version control to avoid security risks.

    Inherits:
        BaseGitIgnoreDefiner: Base class providing method to add .gitignore rules.
    """
    
    def define (
        self,
        security: bool,
    ) -> str:
        
        """
        Generate .gitignore section for security-related files.

        Args:
            security (bool): Whether to include security-related files in the .gitignore file.

        Returns:
            str: The formatted ignore section for security files,
                or an empty string if not enabled.
        """
        
        if security:
            return super().add_ignorance (
                [
                    '.env',
                    '.env.*',
                    'config.yaml',
                    'secrets.json',
                    'secrets.env',
                ]
            )