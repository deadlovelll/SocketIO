import grpc
import os

class GRPCHandler:
    
    @staticmethod
    async def start_grpc_server (
        grpc_server,
        grpc_port
    ) -> None:
        
        """
        Starts the gRPC server dynamically if gRPC support exists.
        """
        
        try:
            from grpc_stub import socketio_pb2_grpc
            from grpc_stub import socketio_pb2

            class SocketServiceServicer(socketio_pb2_grpc.SocketServiceServicer):
                async def Echo(self, request, context):
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