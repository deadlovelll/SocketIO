import sys
import json

from commands.grpc.grpc_creator import GRPCCreator
from commands.docker.dockerfile.dockerfile_creator.dockerfile_creator import DockerfileCreator
from commands.docker.dockerignore.dockerignore_creator.dockerignore_creator import DockerIgnoreCreator
from commands.elk.elk.elk_config_creator import ELKConfigCreator
from commands.git.gitignore.gitignore_creator.gitignore_creator import GitIgnoreCreator
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_creator.pre_commit_hooks_creator import PreCommitHooksCreator

class CommandController:
    
    command_map = {
        'create_grpc_protocol': GRPCCreator.create_grpc_protocol,
        'createdockerfile': DockerfileCreator.create_file,
        'createdockerignore': DockerIgnoreCreator.create_file,
        'createelastic': ELKConfigCreator.create_elk_config,
        'creategitignore': GitIgnoreCreator.create_file,
        'createprecommithooks': PreCommitHooksCreator.create_file,
    }
    
    @staticmethod
    def main():
        if len(sys.argv) > 1:
            command = sys.argv[1]
            arguments_map = CommandController.parse_arguments(sys.argv[2:])
            CommandController.command_map[command](**arguments_map)
            
    @staticmethod
    def parse_arguments (
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