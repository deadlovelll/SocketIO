"""
BaseCommand module.

Defines the abstract base class for all commands in the SocketIO framework.
"""

from abc import ABC, abstractmethod


class BaseCommand(ABC):
    
    """
    Abstract base class for command execution in the SocketIO CLI.

    This class provides a unified interface for handling command-line
    commands and storing user-defined options.
    """

    def __init__ (
        self, 
        **options,
    ) -> None:
        
        """
        Initialize the base command with user-provided options.

        Args:
            **options: Arbitrary keyword arguments representing command options.
        """
        
        self.options = options
        super().__init__()

    @abstractmethod
    def execute(
        self,
    ) -> None:
        
        """
        Abstract method to execute the command logic.

        All subclasses must implement this method.
        """
        
        ...
