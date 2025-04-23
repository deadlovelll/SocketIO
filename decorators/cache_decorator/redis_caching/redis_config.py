"""
RedisConfig module.

Defines a strongly typed configuration object for setting up a Redis client.
This configuration supports all major connection parameters, including TCP, 
Unix socket, SSL, retry strategies, and custom connection pools.

Used for dependency injection into RedisCaching and other Redis-based components.
"""

from typing import NamedTuple, Mapping, Literal, Optional, List, Type
from redis.retry import Retry
from redis.connection import ConnectionPool
from redis.exceptions import RedisError


class RedisConfig(NamedTuple):
    
    """
    Represents the Redis client configuration.

    Attributes:
        url (str): Full Redis connection URL.
        host (Optional[str]): Redis server host.
        port (Optional[int]): Redis server port.
        db (Optional[int]): Redis database number.
        password (Optional[str]): Password for authentication.
        
        socket_timeout (Optional[float]): Timeout for read operations.
        socket_connect_timeout (Optional[float]): Timeout for connection attempts.
        socket_keepalive (Optional[bool]): Whether to use TCP keepalive.
        socket_keepalive_options (Optional[Mapping[str, int | str]]): TCP keepalive options.

        connection_pool (Optional[ConnectionPool]): Custom connection pool.
        unix_socket_path (Optional[str]): Path to Unix socket (overrides host/port if provided).
        encoding (str): Encoding used for data sent to Redis.
        encoding_errors (str): Error handling strategy for encoding.
        charset (Optional[str]): Deprecated alias for `encoding`.
        errors (Optional[str]): Deprecated alias for `encoding_errors`.
        decode_responses (Literal[True]): Whether to decode bytes to strings.
        
        retry_on_timeout (bool): Whether to retry on socket timeout.
        retry_on_error (Optional[List[Type[RedisError]]]): Retry on specified RedisError subclasses.
        
        ssl (bool): Whether to use SSL for connections.
        ssl_keyfile (Optional[str]): Path to the SSL key file.
        ssl_certfile (Optional[str]): Path to the SSL certificate file.
        ssl_cert_reqs (Optional[str | int]): Whether SSL certificates are required.
        ssl_ca_certs (Optional[str]): Path to the CA certificate bundle.
        ssl_check_hostname (bool): Whether to verify the server’s hostname.

        max_connections (Optional[int]): Maximum number of simultaneous connections.
        single_connection_client (bool): Use a single persistent connection.
        health_check_interval (float): Interval for connection health checks.
        client_name (Optional[str]): Optional name for the client connection.
        username (Optional[str]): Username for ACL-based authentication.
        retry (Optional[Retry]): Retry strategy.
    """
    
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
