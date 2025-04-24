"""
This module defines the `GitIgnoreCreator` class, which aggregates 
multiple `.gitignore` section definers and creates a complete 
.gitignore file based on user-specified options.

Each definer handles a specific context (e.g., virtual environments, IDEs, Docker, etc.)
and generates the corresponding ignore patterns.
"""

from typing import Any, Dict, override, Type

from commands.git.gitignore.gitignore_definers.gitignore_definers import (
    GitIgnoreVenvDefiner,
    GitIgnoreLogsDefiner,
    GitIgnorePackagingDefiner,
    GitIgnoreOsSpecificFilesDefiner,
    GitIgnoreIDEFilesDefiner,
    GitIgnoreCoverageDefiner,
    GitIgnoreDockerDefiner,
    GitIgnoreGRPCDefiner,
    GitIgnoreJupyterCopyBookDefiner,
    GitIgnoreTestingDefiner,
    GitIgnoreSecurityDefiner,
    GitIgnoreCachesDefiner,
    GitIgnoreByteCodeDefiner
)

from commands.base_command.base_command import BaseCommand
from utils.static.privacy.privacy import privatemethod
from utils.static.privacy.protected_class import ProtectedClass


class GitIgnoreCreator(ProtectedClass, BaseCommand):
    
    """
    Generates a .gitignore file by combining sections 
    from multiple domain-specific definers based on provided options.
    
    Inherits from:
        BaseCommand: Abstract base class for commands with an `execute()` method.

    Attributes:
        definers (Dict[str, Type]): A mapping from option names to definer classes.
    """
    
    def __init__ (
        self, 
        **options: Any,
    ) -> None:
        
        """
        Initializes the GitIgnoreCreator with a mapping of definer options.

        Args:
            **options (Any): Keyword arguments representing which sections to include in the .gitignore.
                             Each key corresponds to a definer name, and the value (truthy) enables it.
        """
        
        super().__init__(**options)
        
        self._definers: Dict[str, Type] = {
            'bytecode_files': GitIgnoreByteCodeDefiner,
            'venv': GitIgnoreVenvDefiner,
            'logs': GitIgnoreLogsDefiner,
            'packaging': GitIgnorePackagingDefiner,
            'os_specific': GitIgnoreOsSpecificFilesDefiner,
            'ide_files': GitIgnoreIDEFilesDefiner,
            'coverage': GitIgnoreCoverageDefiner,
            'caches': GitIgnoreCachesDefiner,
            'docker': GitIgnoreDockerDefiner,
            'grpc': GitIgnoreGRPCDefiner,
            'jupyter_cp': GitIgnoreJupyterCopyBookDefiner,
            'testing': GitIgnoreTestingDefiner,
            'security': GitIgnoreSecurityDefiner,
        }
    
    @privatemethod
    def _create_file_text (
        self,
    ) -> str:
        
        """
        Generates the full text for the .gitignore file based on enabled definers.

        Returns:
            str: Concatenated .gitignore sections.
        """
        
        sections = []

        for key, value in self.options.items():
            definer_cls = self.definers.get(key)
            if definer_cls and value:
                section = definer_cls().define(value)
                if section:
                    sections.append(section)

        return '\n\n'.join(sections).strip()
    
    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Creates or overwrites the .gitignore file with generated content.
        """
        
        content = self._create_file_text()

        with open('.gitignore', 'w') as f:
            f.write(content)
            
        print('.gitignore has been created.')
        
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Executes the creation of the .gitignore file.
        Calls `create_file` internally.
        """
        
        self._create_file()