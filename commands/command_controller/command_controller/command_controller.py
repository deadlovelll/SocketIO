import sys

from typing import Callable, Any

from commands.grpc.grpc_creator import GRPCCreator
from commands.docker.dockerfile.dockerfile_creator.dockerfile_creator import DockerfileCreator
from commands.docker.dockerignore.dockerignore_creator.dockerignore_creator import DockerIgnoreCreator
from commands.elk.elk.elk_config_creator import ELKConfigCreator
from commands.git.gitignore.gitignore_creator.gitignore_creator import GitIgnoreCreator
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_creator.pre_commit_hooks_creator import PreCommitHooksCreator
from commands.git.pre_commit.black.black_creator.black_creator import BlackCreator
from commands.git.pre_commit.isort.isort_creator.isort_creator import IsortCreator
from commands.git.pre_commit.mypy.mypy_creator.mypy_creator import MypyCreator
from commands.git.pre_commit.pre_commit.pre_commit_creator.pre_commit_creator import PreCommitConfigCreator

from commands.command_controller.command_mapper.command_mapper import CommandArgumentMapper

class CommandController:
    
    def __init__ (
        self,
    ) -> None:
        
        self.argument_mapper = CommandArgumentMapper()
        
        self.command_map: dict[str, Callable[..., Any]] = {
            # 'create_grpc_protocol': GRPCCreator.create_grpc_protocol,
            # 'createdockerfile': DockerfileCreator.create_file,
            # 'createdockerignore': DockerIgnoreCreator.create_file,
            # 'createelastic': ELKConfigCreator.create_elk_config,
            # 'creategitignore': GitIgnoreCreator.create_file,
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
            self.print_help()
            return

        command = sys.argv[1]
        args = self.parse_arguments(sys.argv[2:])
        print(args)

        if command not in self.command_map:
            print(f"Unknown command: '{command}'")
            self.print_help()
            return

        handler = self.command_map[command](**args)
        handler.execute()

            
    def parse_arguments (
        self,
        args: list[str],
    ) -> dict[str, Any]:
        
        return self.argument_mapper.parse_arguments(args)

    def print_help (
        self,
    ) -> None:
        
        print("Available commands:\n")
        for cmd in self.command_map:
            print(f"  - {cmd}")