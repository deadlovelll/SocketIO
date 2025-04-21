"""
PostgreSQL Driver Base Message Handler

This module defines an abstract base class `PostgresDriverBaseMessageHandler`,
which provides a unified interface for implementing PostgreSQL protocol message handlers.

It is designed to be subclassed by concrete handlers that process specific types
of messages received from the PostgreSQL server (e.g., authentication, error, query results).
"""

from abc import ABC, abstractmethod


class PostgresDriverBaseMessageHandler(ABC):
    
    """
    Abstract base class for all PostgreSQL message handlers.

    Any subclass must implement the `handle` method, which defines
    how to process a specific type of server message.
    """
    
    @abstractmethod
    def handle():
        """
        Handle the incoming message payload.

        This method must be implemented by subclasses to define
        the actual message handling logic.

        Args:
            *args: Positional arguments passed to the handler.
            **kwargs: Keyword arguments passed to the handler.
        """
        ...