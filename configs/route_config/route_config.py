"""
RouteConfig dataclass

This module defines the RouteConfig dataclass, which encapsulates all
the configuration needed for registering an HTTP/WebSocket route or endpoint
in the SocketIO framework or similar web servers. It supports route handler binding,
middleware, protection, concurrency, caching, rate limiting, and hooks.
"""

from dataclasses import dataclass
from typing import Callable, Optional, Any, List


@dataclass
class RouteConfig:
    
    """
    RouteConfig defines the configuration for a single route/endpoint.

    Attributes:
        path (str): The URI path for this route (e.g., '/api/items').
        handler (Callable[..., None]): The handler function for the route.
        methods (List[str]): A list of HTTP methods allowed for this route (e.g., ['GET', 'POST']).
        protected (bool): If True, route requires authentication/authorization.
        response_type (Any): The expected type of the response (e.g., dict, str, or custom model).
        on_startup (Optional[Callable[..., None]]): Optional startup hook for this route.
        on_shutdown (Optional[Callable[..., None]]): Optional shutdown hook for this route.
        IOBound (bool): If True, marks the handler as IO-bound (for thread pool/executor separation).
        CPUBound (bool): If True, marks the handler as CPU-bound (for process pool/executor separation).
        rate_limitation (bool): Enables rate limiting on this route if True.
        debounce (int): Minimum time (ms) to wait before accepting new requests (debouncing).
        caching (Optional[Any]): Caching configuration or decorator (in-memory, Redis, etc).
        logging (Optional[bool]): If True, enables logging for this route.
    """
    
    path: str
    handler: Callable[..., None]
    methods: List[str]
    protected: bool
    response_type: Any
    on_startup: Optional[Callable[..., None]] = None
    on_shutdown: Optional[Callable[..., None]] = None
    IOBound: bool = False
    CPUBound: bool = False
    rate_limitation: bool = False
    debounce: int = 0
    caching: Optional[Any] = None
    logging: Optional[bool] = None
