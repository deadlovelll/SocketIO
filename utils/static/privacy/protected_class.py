import inspect

from typing import Any

from exceptions.static_exceptions.static_exceptions import SocketIOStaticAccessException
from utils.static.privacy.privacy import privatemethod

class ProtectedClass:
    
    def __getattribute__ (
        self,
        name,
    ) -> Any:
        
        if name.startswith('_') and not name.startswith('__'):
            import inspect
            stack = inspect.stack()
            try:
                caller_frame = stack[1].frame
                caller_self = caller_frame.f_locals.get('self')
                if caller_self is not self:
                    raise SocketIOStaticAccessException(name)
            finally:
                del stack  
        return super().__getattribute__(name)