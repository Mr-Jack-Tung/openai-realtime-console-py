import logging
from datetime import datetime
from enum import Enum

from typing_extensions import Literal


class Color:
    RESET = "\033[0m"
    GREY = "\033[90m"
    LIGHT_BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[35m"
    RED = "\033[91m"


class Verbosity(Enum):
    NORMAL = 1
    VERBOSE = 2
    DEBUG = 3

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Verbosity):
            return self.value > other.value
        raise ValueError(f"Cannot compare {self} with {other}")

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Verbosity):
            return self.value < other.value
        raise ValueError(f"Cannot compare {self} with {other}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Verbosity):
            return self.value == other.value
        raise ValueError(f"Cannot compare {self} with {other}")


class RealtimeClientLogger:
    def __init__(
        self, name: str | None, verbosity: Verbosity, level: int = logging.DEBUG
    ):
        self.verbosity = verbosity
        self.logger = self._init_logger(name, level)

    def _init_logger(self, name: str | None, level: int):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def debug(self, message: str, *args, **kwargs):
        prefix = f"{Color.GREY}[{self._get_timestamp()}]{Color.RESET}"
        formatted_message = f"{prefix} {message}"
        self.logger.debug(formatted_message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        prefix = f"{Color.GREY}[{self._get_timestamp()}]{Color.RESET}"
        formatted_message = f"{prefix} {message}"
        self.logger.info(formatted_message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        prefix = f"{Color.GREY}[{self._get_timestamp()}]{Color.RESET}"
        formatted_message = f"{prefix} {Color.YELLOW}WARNING - {message}{Color.RESET}"
        self.logger.warning(formatted_message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        prefix = f"{Color.GREY}[{self._get_timestamp()}]{Color.RESET}"
        formatted_message = f"{prefix} {Color.RED}ERROR - {message}{Color.RESET}"
        self.logger.error(formatted_message, *args, **kwargs)

    def log_event(self, event: dict, log_type: Literal["server", "client"]):
        suffix = ""
        if self.verbosity > Verbosity.NORMAL:
            suffix = f" {event}"

        if log_type == "server":
            prefix = f"{Color.GREEN}↓ Server:{Color.RESET}"
        elif log_type == "client":
            prefix = f"{Color.LIGHT_BLUE}↑ Client:{Color.RESET}"

        formatted_message = f"{prefix} {event['type']}{suffix}"
        self.debug(formatted_message)

    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_logger(
    name: str | None = None, verbosity: int = 1, debug_level: int = logging.DEBUG
) -> RealtimeClientLogger:
    """
    Get a configured logger instance.

    Args:
        name (str | None): The name of the logger. If None, returns the root logger.
        verbosity (int): The verbosity level. 1 is normal, 2 is more verbose, 3 is debug.
        debug_level (int): The debug level. Defaults to logging.DEBUG.

    Returns:
        RealtimeClientLogger: Configured logger instance
    """
    return RealtimeClientLogger(
        name or "realtime_client", Verbosity(verbosity), debug_level
    )
