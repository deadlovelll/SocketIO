import sys
from typing import Any, Callable

from commands.command_controller.command_mapper.command_mapper import CommandArgumentMapper
from commands.commands import (
    BlackCreator,
    DockerfileCreator,
    DockerIgnoreCreator,
    ELKConfigCreator,
    GitIgnoreCreator,
    GRPCCreator,
    IsortCreator,
    MypyCreator,
    PreCommitConfigCreator,
    PreCommitHooksCreator,
)

from utils.static.privacy import (
    ProtectedClass,
    privatemethod,
)


class CommandController(ProtectedClass):
    
    def __init__ (
        self,
    ) -> None:
        
        self._argument_mapper = CommandArgumentMapper()
        
        self._command_map: dict[str, Callable[..., Any]] = {
            'create_grpc_protocol': GRPCCreator,
            'createdockerfile': DockerfileCreator,
            'createdockerignore': DockerIgnoreCreator,
            'createelastic': ELKConfigCreator,
            'creategitignore': GitIgnoreCreator,
            'createprecommithooks': PreCommitHooksCreator,
            'createblackhook': BlackCreator,
            'createisorthook': IsortCreator,
            'createmypyhook': MypyCreator,
            'createprecommit': PreCommitConfigCreator,
        }
    
    def run (
        self,
    ) -> None:
        
        if len(sys.argv) < 2:
            self._print_help()
            return

        command = sys.argv[1]
        args = self._parse_arguments(sys.argv[2:])

        if command not in self._command_map:
            print(f"Unknown command: '{command}'")
            self._print_help()
            return

        handler = self._command_map[command](**args)
        handler.execute()

    @privatemethod      
    def _parse_arguments (
        self,
        args: list[str],
    ) -> dict[str, Any]:
        
        return self._argument_mapper.parse_arguments(args)

    @privatemethod
    def _print_help (
        self,
    ) -> None:
        
        print("Available commands:\n")
        for cmd in self.command_map:
            print(f"  - {cmd}")