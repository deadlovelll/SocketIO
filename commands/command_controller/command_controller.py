import sys
import json

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

class CommandController:
    
    def __init__ (
        self,
    ) -> None:
        
        self.command_map: dict[str, Callable[..., Any]] = {
            'create_grpc_protocol': GRPCCreator.create_grpc_protocol,
            'createdockerfile': DockerfileCreator.create_file,
            'createdockerignore': DockerIgnoreCreator.create_file,
            'createelastic': ELKConfigCreator.create_elk_config,
            'creategitignore': GitIgnoreCreator.create_file,
            'createprecommithooks': PreCommitHooksCreator.create_file,
            'createblackhook': BlackCreator.create_file,
            'createisorthook': IsortCreator.create_file,
            'createmypyhook': MypyCreator.create_file,
            'createprecommit': PreCommitConfigCreator.create_file,
        }
    
    def run (
        self,
    ) -> None:
        
        if len(sys.argv) < 2:
            self.print_help()
            return

        command = sys.argv[1]
        args = self.parse_arguments(sys.argv[2:])

        if command not in self.command_map:
            print(f"Unknown command: '{command}'")
            self.print_help()
            return

        handler = self.command_map[command]
        handler(**args)

            
    def parse_arguments (
        self,
        args: list[str],
    ) -> dict:
        
        arguments_map = {}
        
        for arg in args:
            key_value = arg.lstrip('--').split('=', 1) 
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else None

            if value:
                if value.lower() in ['true', 'false']:  
                    value = value.lower() == 'true'
                elif value.startswith('[') and value.endswith(']'):  
                    value = json.loads(value) 
                elif ',' in value:  
                    value = [
                        int(v.strip()) 
                        if v.strip().lstrip('-').isdigit() 
                        else v.strip() 
                        for v in value.split(',')
                    ]
                elif value.lstrip('-').isdigit():  
                    value = [int(value)]
            arguments_map[key] = value
        
        return arguments_map

    def print_help (
        self,
    ) -> None:
        
        print("Available commands:\n")
        for cmd in self.command_map:
            print(f"  - {cmd}")