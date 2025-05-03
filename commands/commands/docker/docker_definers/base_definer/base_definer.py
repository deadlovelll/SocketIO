"""
BaseDockerDefiner module.

This abstract base class defines the contract for all Dockerfile section definers
used to dynamically construct Dockerfile content.
"""

from abc import ABC, abstractmethod


class BaseDockerDefiner(ABC):
    
    """
    Abstract base class for Dockerfile definers.

    Subclasses must implement the `define` method, which returns a string representation
    of a specific Dockerfile section based on input configuration.
    """

    @abstractmethod
    def define (
        self,
        *args,
        **kwargs,
    ) -> str:
        
        """
        Abstract method to define a section of a Dockerfile.

        Args:
            *args: Positional arguments required for definition.
            **kwargs: Keyword arguments for dynamic content generation.

        Returns:
            str: A Dockerfile snippet or block.
        """
        
        ...
