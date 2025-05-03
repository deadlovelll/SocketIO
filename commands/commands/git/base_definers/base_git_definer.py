"""
Provides an abstract base class for defining Git-related configuration or behavior.
This class is intended to be subclassed by concrete implementations that encapsulate
custom Git setup logic.
"""

from abc import ABC, abstractmethod


class BaseGitDefiner(ABC):
    
    """
    Abstract base class for defining Git setup logic.

    Subclasses should implement the `define` method to perform any required
    Git initialization, configuration, or preparation logic (e.g., creating
    `.gitignore` files, setting up remotes, etc.).
    """

    @abstractmethod
    def define (
        self,
    ) -> None:
        
        """
        Defines the Git-related setup or configuration logic.

        This method must be implemented by subclasses to perform specific Git
        initialization tasks.

        Raises:
            NotImplementedError: If the subclass does not override this method.
        """
        
        ...
