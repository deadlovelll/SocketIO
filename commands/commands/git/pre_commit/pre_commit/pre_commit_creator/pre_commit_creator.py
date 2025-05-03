"""
Module that defines the PreCommitConfigCreator class, responsible for generating 
a full `.pre-commit-config.yaml` file based on a user-defined configuration.

This class dynamically selects and executes hook-specific creators such as 
Black, Isort, Mypy, and optional custom hooks, depending on configuration flags.
"""

from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.commands.git.pre_commit.black.black_creator.black_creator import BlackCreator
from commands.commands.git.pre_commit.isort.isort_creator.isort_creator import IsortCreator
from commands.commands.git.pre_commit.mypy.mypy_creator.mypy_creator import MypyCreator
from commands.commands.git.pre_commit.pre_commit.pre_commit_config.pre_commit_config import PreCommitConfig
from commands.commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_creator.pre_commit_hooks_creator import PreCommitHooksCreator
from commands.base_command.base_command import BaseCommand

from utils.static.privacy import (
    privatemethod,
    ProtectedClass,
)


class PreCommitConfigCreator (
    BaseCommand, 
    FileCreator,
    ProtectedClass,
):
    
    """
    Creates pre-commit configuration files by delegating the task to specific hook creators
    such as Black, Isort, and Mypy, based on provided configuration options.

    This class uses PreCommitConfig to determine which hook creators to activate.

    Attributes:
        PRE_COMMIT_MAP (dict[str, Type[BaseCommand]]): A mapping from configuration keys
            to their corresponding hook creator classes.
    """
    
    def __init__ (
        self,
        **options: Any,
    ) -> None:
        
        """
        Initializes the PreCommitConfigCreator with dynamic options for configuring
        which hooks should be created.

        Args:
            **options: Arbitrary keyword arguments used to configure each hook creator.
        """
        
        super().__init__(**options)
    
        self._PRE_COMMIT_MAP = {
            'black': BlackCreator,
            'precommithooks': PreCommitHooksCreator,
            'isort': IsortCreator,
            'mypy': MypyCreator,
        }

    @privatemethod
    def _create_file (
        self,
    ) -> None:
        
        """
        Instantiates and executes the appropriate hook creator classes
        based on the flags in the PreCommitConfig.

        Each creator is responsible for generating its own section in the
        `.pre-commit-config.yaml` file.
        """
        
        config = PreCommitConfig(**self.options)

        for key, creator in self._PRE_COMMIT_MAP.items():
            if getattr(config, key, False):
                creator(**self.options).execute()
    
    @override            
    def execute (
        self,
    ) -> None:
        
        """
        Executes the pre-commit configuration creation process by
        calling the `create_file` method.
        """
        
        self._create_file()