"""
PostgreSQL Driver Configuration

This module defines a configuration dataclass used to initialize and connect a custom
PostgreSQL driver. It encapsulates connection-related parameters such as host, port,
user credentials, and database name.
"""

from dataclasses import dataclass


@dataclass
class PostgresDriverConfig:
    
    """
    Configuration for connecting to a PostgreSQL server.

    Attributes:
        host (str): The hostname or IP address of the PostgreSQL server.
        port (int): The port number to connect to (default: 5432).
        user (str): The username to authenticate with.
        password (str): The corresponding password for the given user.
        database_name (str): The target database name to connect to.
    """
    
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    database_name: str = 'postgres'