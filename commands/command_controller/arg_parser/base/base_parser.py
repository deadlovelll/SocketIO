"""
BaseArgumentParser module.

Defines the abstract base class for argument parsers used in the command-line interface
of the SocketIO framework.
"""

from abc import ABC, abstractmethod


class BaseArgumentParser(ABC):
    
    """
    Abstract base class for command-line argument parsers.

    Subclasses should implement logic to determine whether they can parse a given string
    and how to convert it into the appropriate Python object.
    """

    @abstractmethod
    def can_parse (
        self, 
        value: str,
    ) -> bool:
        
        """
        Determines whether the parser can handle the given input value.

        Args:
            value (str): The input string to be checked.

        Returns:
            bool: True if this parser can handle the value, False otherwise.
        """
        
        ...

    @abstractmethod
    def parse (
        self, 
        value: str,
    ) -> object:
        
        """
        Parses the given string into a corresponding Python object.

        Args:
            value (str): The input string to be parsed.

        Returns:
            object: The parsed value, converted into an appropriate Python type.
        """
        
        ...
