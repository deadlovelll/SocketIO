from dataclasses import dataclass
from typing import Callable, Optional, Any

@dataclass
class RouteConfig:
    path: str
    handler: Callable[..., None]
    methods: list[str]
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