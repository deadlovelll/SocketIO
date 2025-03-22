from typing import Callable

class SocketIORouter:
    
    async def add_api_route (
        self,
        path: str, 
        methods: list[str],
        protected: bool,
        response_type,
        on_startup: Callable[..., None],
        on_shutdown: Callable[..., None],
        IOBound: bool,
        CPUBound: bool,
        rate_limitation: bool,
        debounce: int,
        caching: None,
        logging: bool = None,
    ) -> None:
        
        pass