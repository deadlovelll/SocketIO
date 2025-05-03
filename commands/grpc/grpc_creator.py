"""
GRPCCreator Module

This module provides utilities to generate and compile a basic gRPC protocol
buffer definition for a sample `SocketService`. It includes file creation,
directory management, and compilation using `grpc_tools.protoc`.
"""

import subprocess
import os
import textwrap

from typing import override

from commands.base_command.base_command import BaseCommand

from utils.static.privacy.privacy import privatemethod


class GRPCCreator(BaseCommand):
    
    """
    GRPCCreator provides static methods to generate and compile gRPC `.proto` files.
    It supports automatic directory creation, `.proto` content generation,
    and stub compilation using `grpc_tools.protoc`.
    """
    
    @privatemethod
    def _create_grpc_protocol (
        self,
    ) -> None:
        
        """
        Executes the complete gRPC setup workflow:
        - Creates stub directory if it does not exist.
        - Creates `.proto` definition file.
        - Compiles the `.proto` file to generate Python stubs.
        """
        
        self._create_grpc_stub_directory()
        self._create_grpc_proto_file()
        self._compile_grpc_proto_file()
    
    @privatemethod
    def _create_grpc_proto_file (
        self,
    ) -> None:
        
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
    
    @privatemethod
    def _compile_grpc_proto_file (
        self,
    ) -> None:
        
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
    
    @privatemethod
    def _create_grpc_stub_directory (
        self,
    ) -> None:
        
        """
        Compiles the `socketio.proto` file to generate Python stubs using grpc_tools.protoc.
        """
        
        os.mkdir('./grpc_stub')
    
    @override
    def execute (
        self,
    ) -> None:
        
        self._create_grpc_protocol()