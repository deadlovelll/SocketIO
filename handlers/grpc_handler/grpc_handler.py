"""
Module for handling gRPC server operations.

This module defines the `GRPCHandler` class, which is responsible for dynamically
starting a gRPC server that listens for incoming requests. It supports handling 
Echo requests through a custom service and sends back the same message received.

The module also handles the scenario where the required gRPC protocol files are 
missing, printing an error message if gRPC support is unavailable.
"""

import grpc
import os


class GRPCHandler:
    
    """
    A class for handling gRPC server operations, including dynamically starting 
    a gRPC server and handling requests via the gRPC protocol.

    The server uses a custom `SocketServiceServicer` to handle Echo requests.
    """

    @staticmethod
    async def start_grpc_server(
        grpc_server, 
        grpc_port: int
    ) -> None:
        
        """
        Starts the gRPC server dynamically if gRPC support is available.

        This method initializes the gRPC server, defines the service, and starts
        listening for incoming requests. If gRPC support is not found, it handles
        the `ModuleNotFoundError` exception by printing a relevant message.

        Args:
            grpc_server: An instance of a gRPC server (will be created within the method).
            grpc_port (int): The port on which the gRPC server will listen for incoming connections.

        Returns:
            None

        Raises:
            ModuleNotFoundError: If the required gRPC protocol files are not found.

        Notes:
            The gRPC server listens for `Echo` requests, where it returns the same message sent in the request.
        """
        
        try:
            from grpc_stub import socketio_pb2_grpc
            from grpc_stub import socketio_pb2

            class SocketServiceServicer(socketio_pb2_grpc.SocketServiceServicer):
                
                """
                gRPC service for handling Echo requests. This class defines the 
                methods that the gRPC server will expose to clients.
                """
                
                async def Echo(self, request, context):
                    
                    """
                    Handles Echo requests from clients, returning the same message sent in the request.

                    Args:
                        request: The request object containing the message from the client.
                        context: The gRPC context for the current RPC call.

                    Returns:
                        EchoResponse: A response containing the same message as the input.
                    """
                    
                    return socketio_pb2.EchoResponse(message=request.message)

            grpc_server = grpc.aio.server()
            servicer = SocketServiceServicer()
            
            socketio_pb2_grpc.add_SocketServiceServicer_to_server (
                servicer, 
                grpc_server,
            )
            
            grpc_server.add_insecure_port(f"[::]:{grpc_port}")
            await grpc_server.start()
            
            os.environ["GRPC_SERVICE_ENABLED"] = "1"
            
            await grpc_server.wait_for_termination()

        except ModuleNotFoundError:
            print("Error: gRPC files not found. Run `python3 socketio.py creagrpcprotocol` first.")