from commands.command_controller.arg_parser.base.base_parser import BaseArgumentParser
from commands.command_controller.arg_parser.type_parser.type_parser import (
    BoolParser,
    ListParser,
    IntParser
)


class ArgumentParser:
    
    def __init__ (
        self,
    ) -> None:
        
        self.parsers: list[BaseArgumentParser] = [
            BoolParser(),
            ListParser(),
            IntParser(),
        ]

    def parse (
        self, 
        value: str,
    ) -> object:
        
        for parser in self.parsers:
            if parser.can_parse(value):
                return parser.parse(value)
        return value 
