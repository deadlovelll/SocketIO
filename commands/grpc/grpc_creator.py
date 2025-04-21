"""
GRPCCreator Module

This module provides utilities to generate and compile a basic gRPC protocol
buffer definition for a sample `SocketService`. It includes file creation,
directory management, and compilation using `grpc_tools.protoc`.
"""

import subprocess
import os
import textwrap


class GRPCCreator:
    
    """
    GRPCCreator provides static methods to generate and compile gRPC `.proto` files.
    It supports automatic directory creation, `.proto` content generation,
    and stub compilation using `grpc_tools.protoc`.
    """
    
    @staticmethod
    def create_grpc_protocol() -> None:
        
        """
        Executes the complete gRPC setup workflow:
        - Creates stub directory if it does not exist.
        - Creates `.proto` definition file.
        - Compiles the `.proto` file to generate Python stubs.
        """
        
        GRPCCreator.create_grpc_stub_directory()
        GRPCCreator.create_grpc_proto_file()
        GRPCCreator.compile_grpc_proto_file()
    
    @staticmethod   
    def create_grpc_proto_file() -> None:
        
        """
        Creates the `grpc_stub` directory if it doesn't already exist.
        """
        
        proto_content = textwrap.dedent("""\
        syntax = "proto3";

        package socketio;

        // The SocketService defines the gRPC service.
        service SocketService {
            // Echo returns the same message sent by the client.
            rpc Echo (EchoRequest) returns (EchoResponse);
        }

        // EchoRequest contains the message to be echoed.
        message EchoRequest {
            string message = 1;
        }

        // EchoResponse contains the echoed message.
        message EchoResponse {
            string message = 1;
        }
        """)

        with open('./grpc_stub/socketio.proto', 'w') as file:
            file.write(proto_content)

        print("socketio.proto file has been created.")
    
    @staticmethod
    def compile_grpc_proto_file() -> None:
        
        """
        Generates a default `socketio.proto` file for a basic Echo gRPC service.
        """
        
        subprocess.run (
            [
                'python', 
                '-m', 
                'grpc_tools.protoc', 
                '--python_out=.', 
                '--grpc_python_out=.', 
                '-I.', 
                './grpc_stub/socketio.proto',
            ]
        )
        
        print("socketio.proto file has been compiled.")
        
    @staticmethod
    def create_grpc_stub_directory() -> None:
        
        """
        Compiles the `socketio.proto` file to generate Python stubs using grpc_tools.protoc.
        """
        
        os.mkdir('./grpc_stub')