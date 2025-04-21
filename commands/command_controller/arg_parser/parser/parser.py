"""
ArgumentParser module.

Provides a unified interface for parsing command-line argument values into proper Python types.
Relies on a set of type-specific parsers implementing `BaseArgumentParser`.
"""

from commands.command_controller.arg_parser.base.base_parser import BaseArgumentParser
from commands.command_controller.arg_parser.type_parser.type_parser import (
    BoolParser,
    ListParser,
    IntParser,
)


class ArgumentParser:
    
    """
    ArgumentParser orchestrates multiple type parsers to convert string inputs into
    appropriate Python objects.

    It checks each parser in order and returns the first successful result.
    If no parser can handle the value, it returns the original string.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the parser with a default set of type parsers: Bool, List, and Int.
        """
        
        self.parsers: list[BaseArgumentParser] = [
            BoolParser(),
            ListParser(),
            IntParser(),
        ]

    def parse (
        self, 
        value: str,
    ) -> object:
        
        """
        Parses the given string using the first matching parser.

        Args:
            value (str): The input value to be parsed.

        Returns:
            object: The parsed Python object if a parser matches, otherwise the original string.
        """
        
        for parser in self.parsers:
            if parser.can_parse(value):
                return parser.parse(value)
        return value
