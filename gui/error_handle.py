import sys
from functools import wraps
from typing import Any, Tuple


def error_handler(func) -> Tuple[Any, str]:

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs), ""
        except Exception:
            return args[0], str(sys.exc_info()[1]).split(",")[4]

    return wrapper
