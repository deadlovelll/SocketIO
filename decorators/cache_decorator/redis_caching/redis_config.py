from typing import NamedTuple, Mapping, Literal, Optional, List, Type
from redis.retry import Retry
from redis.connection import ConnectionPool
from redis.exceptions import RedisError

class RedisConfig(NamedTuple):
    
    url: str
    host: Optional[str] = None
    port: Optional[int] = None
    db: Optional[int] = None
    password: Optional[str] = None
    
    socket_timeout: Optional[float] = None
    socket_connect_timeout: Optional[float] = None
    socket_keepalive: Optional[bool] = None
    socket_keepalive_options: Optional[Mapping[str, int | str]] = None
    
    connection_pool: Optional[ConnectionPool] = None
    unix_socket_path: Optional[str] = None
    encoding: str = "utf-8"
    encoding_errors: str = "strict"
    charset: Optional[str] = None
    errors: Optional[str] = None
    decode_responses: Literal[True] = True
    retry_on_timeout: bool = False
    retry_on_error: Optional[List[Type[RedisError]]] = None
    
    ssl: bool = False
    ssl_keyfile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_cert_reqs: Optional[str | int] = None
    ssl_ca_certs: Optional[str] = None
    ssl_check_hostname: bool = False
    
    max_connections: Optional[int] = None
    single_connection_client: bool = False
    health_check_interval: float = 0.0
    client_name: Optional[str] = None
    username: Optional[str] = None
    retry: Optional[Retry] = None
