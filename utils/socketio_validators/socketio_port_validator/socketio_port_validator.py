"""
Port validation utility for the SocketIO framework.

Provides logic to validate if a given port number is acceptable for use,
preventing collisions or security risks associated with certain port ranges.
"""

from exceptions.socketio_exceptions.socketio_exceptions import (
    SocketIOForbieddenPortError,
    SocketIOInproperPortError,
)


class SocketIOPortValidator:
    
    """
    A static utility class to validate port numbers used by the SocketIO server.
    
    It ensures ports are not reserved, out of range, or fall into dynamic/ephemeral ranges.
    """

    @staticmethod
    def verify_port_validity (
        port: int,
    ) -> int:
        
        """
        Verifies the given port is valid and not in a restricted range.

        Args:
            port (int): The port number to validate.

        Returns:
            int: The validated port number.

        Raises:
            SocketIOForbieddenPortError: If the port is in the reserved (0–1023) range.
            SocketIOInproperPortError: If the port is not between 0 and 65535.
        """
        
        forbidden_ports = list(range(0, 1024)) 
        dynamic_ports = list(range(49152, 65536))
        
        if port in forbidden_ports:
            raise SocketIOForbieddenPortError(port)

        if port < 0 or port > 65535:
            raise SocketIOInproperPortError(port)

        if port in dynamic_ports:
            print(f"⚠️ Port {port} belongs to the dynamic range (49152–65535), conflicts may exist.")

        return port
