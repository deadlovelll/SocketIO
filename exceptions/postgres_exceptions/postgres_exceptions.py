from exceptions.base_exception.socketio_exception import SocketIOException

class SocketIOPostgresDriverException(SocketIOException):
    
    def __init__ (
        self,
        sqlstate: str,
        message: str,
    ) -> None:
        
        message = f"""
{'#' * 80}
# ERROR: PostgreSQL error {sqlstate}: {message}.          #
#                                                                              #
# See the full list of Postgres SQLSTATE codes here:                           #
# https://www.postgresql.org/docs/current/errcodes-appendix.html               #
#                                                                              #
# If you're not sure what this means, consult the above appendix.              #
{'#' * 80}
"""
        super().__init__(message)