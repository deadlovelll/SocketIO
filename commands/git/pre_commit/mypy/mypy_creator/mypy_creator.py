"""
This module defines the `MypyCreator` class, which generates or updates a Mypy hook
entry in a `.pre-commit-config.yaml` file. The configuration is dynamically constructed
from a `MypyConfig` dataclass and supports automatic version resolution from GitHub
if no specific revision is supplied.
"""

from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.mypy.mypy_config.mypy_config import MypyConfig
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator


from utils.static.privacy import (
    privatemethod,
)


class MypyCreator(BaseHookCreator, FileCreator):
    
    """
    Creates or updates a pre-commit configuration entry for Mypy.

    Inherits from:
        BaseHookCreator: Provides base logic for determining whether to create or update a file.
        FileCreator: Interface enforcing the implementation of file creation logic.
    """
        
    @override
    @privatemethod
    def _generate_args (
        self,
        config: MypyConfig = MypyConfig(),
    ) -> list[str]:
        
        """
        Generate the list of CLI arguments to be used in the Mypy hook.

        Args:
            config (MypyConfig): The configuration dataclass for Mypy.

        Returns:
            list[str]: A list of command-line arguments.
        """
        
        hooks = [
            f'--{hook}' for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    @privatemethod
    def _create_file_text (
        self,
        config: MypyConfig = MypyConfig(),
    ) -> dict[str, Any]:
        
        """
        Create the structure for the YAML hook entry for Mypy.

        Args:
            config (MypyConfig): The configuration to be embedded in the YAML.

        Returns:
            dict[str, Any]: Dictionary representing the YAML structure for Mypy.
        """
        
        hooks = self._generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': {
                        'id': 'mypy',
                        'args': hooks,
                    },
                }
            ]
        }
    
    @override
    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Create or update the `.pre-commit-config.yaml` file with the Mypy hook.

        This method checks if the file exists and decides whether to create or update.
        """
        
        text_dump = self._prepare_text_dump()
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        file_exist = pre_commit_file.exists()
        self.file_map[file_exist](text_dump)
    
    @override
    @privatemethod
    def _prepare_text_dump (
        self,
    ) -> dict[str, Any]:
        
        """
        Prepare the hook configuration structure based on provided options.

        Returns:
            dict[str, Any]: A dictionary representing the final structure to dump to YAML.
        """
        
        config = MypyConfig(self.options)
        text = self._create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Execute the MypyCreator lifecycle to ensure the pre-commit hook is installed.

        This acts as the main entry point when using the object programmatically.
        """
        
        self.create_file()
        