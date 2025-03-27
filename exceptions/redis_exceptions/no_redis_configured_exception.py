from exceptions.base_exception.socketio_exception import SocketIOException

class NoRedisConfiguredException(SocketIOException):
    
    def __init__ (
        self, 
        message = "No redis configured. Are you sure that you defined redis config with RedisConfig?"
    ) -> None:
        
        super().__init__(message)