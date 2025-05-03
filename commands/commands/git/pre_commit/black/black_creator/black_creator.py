"""
Module for generating or updating a pre-commit hook configuration for the Black formatter.

This module provides the `BlackCreator` class which integrates with the pre-commit framework.
It dynamically constructs configuration for the Black Python formatter using options provided
via `BlackConfig`, and implements hook creation logic inherited from `BaseHookCreator`.
"""

from pathlib import Path
from typing import override, Any

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.commands.git.pre_commit.black.black_config.black_config import BlackConfig
from commands.commands.git.pre_commit.base.base_hook_creator import BaseHookCreator

from utils.static.privacy import (
    privatemethod,
    ProtectedClass
)


class BlackCreator (
    BaseHookCreator, 
    FileCreator,
    ProtectedClass,
):
    
    """
    Hook creator for the Black Python formatter.

    Inherits from `BaseHookCreator` and implements methods to generate arguments,
    configuration content, and handle creation or updating of `.pre-commit-config.yaml`.
    """
    
    def __init__ (
        self, 
        **options: Any,
    ) -> None:
        
        """
        Initializes a new instance of the BlackCreator with CLI-style flag mapping.

        Args:
            **options: Configuration options passed to BlackConfig.
        """
        
        super().__init__(**options)
        self._flag_map = {
            'skip_string_normalization': '--skip-string-normalization',
            'skip_magic_trailing_comma': '--skip-magic-trailing-comma',
            'check': '--check',
            'diff': '--diff',
            'preview': '--preview',
            'verbose': '--verbose',
            'quiet': '--quiet',
            'fast': '--fast',
        }
    
    @override
    @privatemethod
    def _generate_args (
        self,
        config: BlackConfig = BlackConfig(),
    ) -> list[str]:
        
        """
        Generates command-line arguments for the Black hook based on provided config.

        Args:
            config (BlackConfig): Configuration instance for Black.

        Returns:
            list[str]: List of CLI flags to pass to the pre-commit hook.
        """
        
        args = [
            f'--line-length={config.line_length}',
            f'--target-version={config.target_version}',
        ]

        for attr, flag in self._flag_map.items():
            if getattr(config, attr):
                args.append(flag)

        return args
    
    @override
    @privatemethod
    def _create_file_text (
        self,
        config: BlackConfig = BlackConfig(),
    ) -> str:
        
        """
        Constructs the YAML content for the Black pre-commit hook.

        Args:
            config (BlackConfig): Configuration instance for Black.

        Returns:
            dict[str, Any]: A dictionary representation of the pre-commit YAML content.
        """
        
        hooks = self._generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': {
                        'id': 'black',
                        'args': hooks
                    },
                },
            ]
        }
    
    @override
    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Creates or updates the `.pre-commit-config.yaml` file at the project root.
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
        Prepares the YAML-compatible dictionary for the Black hook configuration.

        Returns:
            dict[str, Any]: YAML-serializable content for pre-commit.
        """
        
        config = BlackConfig(**self.options)
        text = self._create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        """
        Main entry point to execute the hook file generation process.
        """
        
        self._create_file()
        