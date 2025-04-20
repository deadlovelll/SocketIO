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
        

class SocketIOPostgresDriverAuthException(SocketIOException):
    
    def __init__ (
        self,
        unknown_code: str
    ) -> None:
        
        message = f"""
{'#' * 72}
# PostgreSQL authentication failed with unknown code: {unknown_code:<6}     #
#                                                                          #
# Refer to the full list of PostgreSQL auth codes:                         #
# → https://www.postgresql.org/docs/current/errcodes-appendix.html         #
#                                                                          #
# Tip: This might indicate protocol mismatch or server misconfiguration.  #
{'#' * 72}
"""
        super().__init__(message)