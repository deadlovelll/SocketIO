"""
CommandArgumentMapper module.

Responsible for transforming raw CLI arguments (e.g., --key=value) into a dictionary
with properly typed Python objects, using the ArgumentParser.
"""

from typing import Any
from commands.command_controller.arg_parser.parser.parser import ArgumentParser


class CommandArgumentMapper:
    
    """
    Parses command-line arguments into a dictionary of key-value pairs with proper types.

    Attributes:
        parser (ArgumentParser): Utility to convert string values into correct Python types.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the CommandArgumentMapper with an instance of ArgumentParser.
        """
        
        self.parser = ArgumentParser()

    def parse_arguments(
        self,
        args: list[str],
    ) -> dict[str, Any]:
        
        """
        Parses a list of command-line arguments into a dictionary.

        Args:
            args (list[str]): List of CLI arguments like ['--flag=true', '--port=8000'].

        Returns:
            dict[str, Any]: Parsed arguments with values cast to appropriate types.
        """
        
        arguments_map = {}

        for arg in args:
            key_value = arg.lstrip('--').split('=', 1)
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else None

            if value is not None:
                value = self.parser.parse(value)

            arguments_map[key] = value

        return arguments_map
