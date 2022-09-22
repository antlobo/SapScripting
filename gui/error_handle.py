import sys
from functools import wraps


def error_handler(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("----------------------------------")
            print(locals())
            print(f"{func.__name__}: {sys.exc_info()}")
            print("----------------------------------")
            return args[0]

    return wrapper
