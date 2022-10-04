from functools import wraps
from typing import Any, Tuple
from pywintypes import com_error


def error_handler(func) -> Tuple[Any, str]:

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs), ""
        except com_error as e:
            return args[0], str(e).split(",")[1]
        except Exception as e:
            return e

    return wrapper
