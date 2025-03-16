import sys
import json

from commands.grpc_creator.grpc_creator import GRPCCreator
from commands.dockerfile_builder.dockerfile_creator.dockerfile_creator import DockerfileFactory

class CommandController:
    
    command_map = {
        'create_grpc_protocol': GRPCCreator.create_grpc_protocol,
        'createdockerfile': DockerfileFactory.create_dockerfile,
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
            key_value = arg.lstrip("--").split("=", 1) 
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else None

            if value:
                if value.lower() in ["true", "false"]:  
                    value = value.lower() == "true"
                elif value.startswith("[") and value.endswith("]"):  
                    value = json.loads(value) 
                elif "," in value:  
                    value = [
                        int(v.strip()) 
                        if v.strip().lstrip("-").isdigit() 
                        else v.strip() 
                        for v in value.split(",")
                    ]
                elif value.lstrip("-").isdigit():  
                    value = [int(value)]
            arguments_map[key] = value
        
        return arguments_map