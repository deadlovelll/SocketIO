from SocketIO.exceptions.base_exception.socketio_exception import SocketIOException

class InvalidRestOperationType(SocketIOException):
    
    def __init__ (
        self, 
        expected: list, 
        got: str
    ) -> None:
        
        message = f"Invalid REST operation type, expected {' '.join(expected)}, got {got}"
        super().__init__(message)