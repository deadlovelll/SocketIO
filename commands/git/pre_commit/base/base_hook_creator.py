"""
base_hook_creator.py

This module defines the abstract base class `BaseHookCreator` used for generating
and managing YAML configuration files for pre-commit hooks.
"""

import yaml
from abc import abstractmethod
from typing import Any

from commands.base_command.base_command import BaseCommand


class BaseHookCreator(BaseCommand):
    
    """
    Abstract base class for generating and managing `.pre-commit-config.yaml` files.

    This class provides a structure for creating or updating pre-commit hook
    configuration files in YAML format. It must be subclassed with implementations
    for generating specific hook content.

    Attributes:
        file_map (dict[bool, Callable]): A mapping that determines whether to create or update 
            the file based on its existence.
    """
    
    def __init__ (
        self, 
        **options: Any,
    ) -> None:
        
        """
        Initializes the BaseHookCreator with provided options.

        Args:
            **options (Any): Arbitrary keyword arguments used to configure the command.
        """
        
        super().__init__(**options)
        self.file_map = {
            False: self.create,
            True: self.update,
        }
    
    @abstractmethod
    def generate_args (
        config,
    ) -> list[str]: 
        
        """
        Abstract method to generate command-line arguments for the hook.

        Args:
            config (Any): Configuration input to determine the arguments.

        Returns:
            list[str]: A list of string arguments required for the hook.
        """
        
        ...
    
    @abstractmethod
    def create_file_text (
        config,
    ) -> str:
        
        """
        Abstract method to generate the text content for the YAML file.

        Args:
            config (Any): Configuration used to render the file content.

        Returns:
            str: The generated file content in YAML string format.
        """
        
        ...
        
    
    @abstractmethod
    def create_file (
        **options,
    ) -> None:
        
        """
        Abstract method to create a `.pre-commit-config.yaml` file.

        Args:
            **options (Any): Options required to create the file.
        """
        
        ...
    
    @abstractmethod
    def prepare_text_dump (
        **options,
    ) -> dict[str, Any]:
        
        """
        Abstract method to prepare the dictionary for YAML dumping.

        Args:
            **options (Any): Options required to prepare the data.

        Returns:
            dict[str, Any]: A dictionary structure for pre-commit hook config.
        """
        
        ...
        
    
    def create (
        self,
        text_dump: str,
    ) -> None:
        
        """
        Creates a new `.pre-commit-config.yaml` file with the provided YAML content.

        Args:
            text_dump (str): The stringified YAML content to write into the file.
        """
                
        with open('.pre-commit-config.yaml', 'w') as f:
            yaml.dump (
                text_dump, 
                f,
                default_flow_style=False, 
                sort_keys=False,
            )
            
        print(f'.pre-commit-config.yaml has been created.')
    
    def update (
        self,
        text_dump: dict[str, Any],
    ) -> None:
        
        """
        Updates the `.pre-commit-config.yaml` file with a new or modified repo entry.

        If the repo already exists, it is updated. If not, it is appended.

        Args:
            text_dump (dict[str, Any]): Dictionary representing the new repo config.
        """
        
        with open('.pre-commit-config.yaml', 'r') as f:
            config = yaml.safe_load(f) or {}
        
        config.setdefault('repos', [])
        
        updated = False
        for i, repo in enumerate(config['repos']):
            if repo.get('repo') == text_dump['repos'][0]['repo']:
                config['repos'][i] = text_dump['repos'][0]
                updated = True
                break

        if not updated:
            config['repos'].append(text_dump['repos'][0])

        with open('.pre-commit-config.yaml', 'w') as f:
            yaml.dump (
                config, 
                f, 
                default_flow_style=False, 
                sort_keys=False,
            )