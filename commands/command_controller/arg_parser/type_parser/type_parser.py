"""
Parsers for command-line argument values.

This module defines a set of parsers for converting raw string arguments
from the command line into their respective Python data types.

Each parser implements the BaseArgumentParser interface and handles a specific type:
- BoolParser:     parses boolean strings ('true', 'false')
- ListParser:     parses JSON-style lists (e.g., '[1, 2, 3]')
- IntParser:      parses integers (including negative)

Usage:
    These parsers are used by the ArgumentParser engine to convert command-line
    arguments (typically of the form `--key=value`) into strongly typed Python
    values.
"""

import json

from typing import Any

from commands.command_controller.arg_parser.base.base_parser import BaseArgumentParser

class BoolParser(BaseArgumentParser):
    
    def can_parse (
        self, 
        value: str,
    ) -> bool:
        
        """
        Check if the given value can be parsed as a boolean.

        Args:
            value (str): The string value to check.

        Returns:
            bool: True if the value is 'true' or 'false' (case-insensitive).
        """
        
        return value.lower() in ['true', 'false']

    def parse (
        self, 
        value: str,
    ) -> bool:
        
        """
        Parse the string into a boolean.

        Args:
            value (str): The string to parse.

        Returns:
            bool: True if 'true', False if 'false'.
        """
        
        return value.lower() == 'true'


class ListParser(BaseArgumentParser):
    
    def can_parse (
        self, 
        value: str,
    ) -> bool:
        
        """
        Check if the given value is a JSON-style list.

        Args:
            value (str): The string to check.

        Returns:
            bool: True if the string starts with '[' and ends with ']'.
        """
        
        return value.startswith('[') and value.endswith(']')

    def parse (
        self, 
        value: str,
    ) -> list[Any]:
        
        """
        Parse a JSON list from the string.

        Args:
            value (str): The string in JSON list format.

        Returns:
            list: The parsed list of items.
        """
        
        return json.loads(value)


class IntParser(BaseArgumentParser):
    
    def can_parse (
        self, 
        value: str,
    ) -> bool:
        
        """
        Check if the value can be parsed as an integer.

        Args:
            value (str): The string to check.

        Returns:
            bool: True if the string is a valid integer.
        """
        
        return value.lstrip('-').isdigit()

    def parse (
        self, 
        value: str,
    ) -> int:
        
        """
        Parse the string into an integer.

        Args:
            value (str): The string to convert.

        Returns:
            int: The parsed integer value.
        """
        
        return int(value)
