"""
This module defines the `IsortCreator` class for setting up the isort pre-commit hook.

It extends a generic base class for hook creation (`BaseHookCreator`) and implements
the `FileCreator` interface, allowing configuration for isort to be programmatically
inserted or updated in the `.pre-commit-config.yaml` file.

The `IsortCreator` class takes an `IsortConfig` dataclass instance to generate
appropriate pre-commit arguments and config structure.
"""

from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.isort.isort_config.isort_config import IsortConfig
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator


class IsortCreator(BaseHookCreator, FileCreator):
    
    """
    A concrete hook creator for the `isort` tool used in Python projects.

    Inherits from `BaseHookCreator` and implements the required methods for
    pre-commit hook generation, including argument assembly and file writing.

    Attributes:
        options (dict): Options used to configure the isort hook.
    """
        
    @override
    def generate_args (
        self,
        config: IsortConfig = IsortConfig(),
    ) -> list[str]:
        
        """
        Generate arguments to be passed to the isort hook based on the config.

        Args:
            config (IsortConfig): Configuration options for isort.

        Returns:
            list[str]: A list of arguments in dictionary format to pass to the hook.
        """
        
        hooks = [
            {'id': hook} for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    def create_file_text (
        self,
        config: IsortConfig = IsortConfig(),
    ) -> str:
        
        """
        Build the YAML structure to be written in the pre-commit config.

        Args:
            config (IsortConfig): Configuration object with version and URL.

        Returns:
            str: YAML-compatible dictionary describing the isort hook.
        """
        
        hooks = self.generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': hooks,
                }
            ]
        }
    
    @override
    def create_file (
        self,
    ) -> None:
        
        """
        Create or update the `.pre-commit-config.yaml` file with isort config.
        """
        
        text_dump = self.prepare_text_dump()
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        file_exist = pre_commit_file.exists()
        self.file_map[file_exist](text_dump)
    
    @override
    def prepare_text_dump (
        self,
    ) -> dict[str, Any]:
        
        """
        Prepare the config dictionary to be written to YAML file.

        Returns:
            dict[str, Any]: Structured config for the pre-commit isort hook.
        """
        
        config = IsortConfig(**self.options)
        text = self.create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Entry point for executing the hook creation logic.
        """
        
        self.create_file()
        