from SocketIO.exceptions.socketio_exceptions.socketio_exceptions import (
    SocketIOForbieddenPortError,
    SocketIOInproperPortError
)

class SocketIOPortValidator:
    
    @staticmethod
    def verify_port_validity (
        port: int,
    ) -> None:
        
        forbidden_ports = list(range(0, 1024)) 
        dynamic_ports = list(range(49152, 65536))
        
        if port in forbidden_ports:
            raise SocketIOForbieddenPortError(port)
        elif port > 65535 or port < 0:
            raise SocketIOInproperPortError(port)
            
        elif port in dynamic_ports:
            print(f"Port {port} belongs to the dynamic range(49152–65535), conflicts may exist.")
        
        return port