"""
This module defines the PreCommitHooksCreator class responsible for generating
a `.pre-commit-config.yaml` section using the official `pre-commit-hooks` repository.

It dynamically builds the list of enabled hooks based on a provided configuration
(PreCommitHooksConfig) and writes the configuration file if necessary.
"""

from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_config.pre_commit_hooks_config import PreCommitHooksConfig

from utils.static.privacy import (
    privatemethod,
    ProtectedClass,
)


class PreCommitHooksCreator (
    BaseHookCreator, 
    FileCreator,
    ProtectedClass,
):
    
    """
    Creates a section for `pre-commit-hooks` in the `.pre-commit-config.yaml` file.

    This class builds a list of enabled hooks based on PreCommitHooksConfig,
    fetches the latest version tag, and writes or updates the configuration file.
    """
    
    @override
    @privatemethod
    def _generate_args (
        self,
        config: PreCommitHooksConfig = PreCommitHooksConfig(),
    ) -> list[dict[str, Any]]:
        
        """
        Generates a list of hooks to be included in the config, based on enabled options.

        Args:
            config (PreCommitHooksConfig): Configuration for standard hooks.

        Returns:
            list[dict]: A list of dictionaries containing hook IDs to include.
        """
        
        hooks = [
            {'id': hook} for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    @privatemethod
    def _create_file_text (
        self,
        config: PreCommitHooksConfig = PreCommitHooksConfig(),
    ) -> dict[str, Any]:
        
        """
        Constructs the YAML content for the `.pre-commit-config.yaml` file.

        Args:
            config (PreCommitHooksConfig): Hook configuration options.

        Returns:
            dict[str, Any]: YAML content to be dumped.
        """
        
        hooks = self._generate_args(config)
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
    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Creates or updates the `.pre-commit-config.yaml` file.

        This method resolves the project root, prepares the text to dump,
        and delegates file creation or update based on file existence.
        """
        
        text_dump = self._prepare_text_dump()
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        file_exist = pre_commit_file.exists()
        self.file_map[file_exist](text_dump)
    
    @override
    @privatemethod
    def prepare_text_dump (
        self,
    ) -> dict[str, Any]:
        
        """
        Prepares the text to be dumped into the YAML file by initializing the config.

        Returns:
            dict[str, Any]: Parsed YAML content ready for file creation.
        """
        
        config = PreCommitHooksConfig(**self.options)
        text = self._create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Executes the full hook creation process.

        This includes preparing configuration, generating hook data,
        and writing the final file.
        """
        
        self.create_file()
        