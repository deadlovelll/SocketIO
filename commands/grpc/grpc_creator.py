import subprocess
import os
import textwrap

class GRPCCreator:
    
    @staticmethod
    def create_grpc_protocol():
        GRPCCreator.create_grpc_stub_directory()
        GRPCCreator.create_grpc_proto_file()
        GRPCCreator.compile_grpc_proto_file()
    
    @staticmethod   
    def create_grpc_proto_file():
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
    def compile_grpc_proto_file():
        
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
    def create_grpc_stub_directory():
        os.mkdir('./grpc_stub')