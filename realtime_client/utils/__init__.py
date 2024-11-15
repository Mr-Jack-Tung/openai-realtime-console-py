from typing_extensions import Coroutine

from .logger import get_logger


def background_task(func: Coroutine):
    """This is just for decoration :)"""

    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)

    return wrapper
