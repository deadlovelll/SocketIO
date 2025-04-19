import inspect

def privatemethod(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1].function
        if caller.startswith('_') or caller == '__init__':
            return func(*args, **kwargs)
        raise RuntimeError(f"Method '{func.__name__}' is private and cannot be accessed externally.")
    return wrapper
