from typing import Literal

from pydantic import Field

from ...models import ErrorDetail
from .base import ServerEvent


class Error(ServerEvent):
    """Returned when an error occurs, which could be a client problem or a server problem.
    Most errors are recoverable and the session will stay open, we recommend to implementors to monitor and log error messages by default.
    """

    event_type: Literal["error"] = Field("error", alias="type")
    """The event type, must be 'error'."""

    error: ErrorDetail
    """Details of the error."""
