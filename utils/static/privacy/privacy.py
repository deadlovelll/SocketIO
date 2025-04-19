import inspect

def privatemethod(method):
    def wrapper(self, *args, **kwargs):
        stack = inspect.stack()
        for frame_info in stack[1:]:
            caller_self = frame_info.frame.f_locals.get('self')
            if isinstance(caller_self, self.__class__):
                return method(self, *args, **kwargs)
        raise RuntimeError(f"Method '{method.__name__}' is private and cannot be accessed externally.")
    return wrapper
