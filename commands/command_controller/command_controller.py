import sys

from commands.grpc_creator.grpc_creator import GRPCCreator
from commands.dockerfile_creator.dockerfile_creator import DockerfileFactory

class CommandController:
    
    command_map = {
        'create_grpc_protocol': GRPCCreator.create_grpc_protocol,
        'createdockerfile': DockerfileFactory.create_dockerfile,
    }
    
    @staticmethod
    def main():
        if len(sys.argv) > 1:
            command = sys.argv[1]
            CommandController.command_map[command]()