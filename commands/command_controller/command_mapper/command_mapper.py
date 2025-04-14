from commands.command_controller.arg_parser.parser.parser import ArgumentParser

from typing import Any

class CommandArgumentMapper:
    
    def __init__ (
        self,
    ) -> None:
        
        self.parser = ArgumentParser()

    def parse_arguments (
        self, 
        args: list[str],
    ) -> dict[str, Any]:
        
        arguments_map = {}

        for arg in args:
            key_value = arg.lstrip('--').split('=', 1)
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else None

            if value is not None:
                value = self.parser.parse(value)

            arguments_map[key] = value

        return arguments_map