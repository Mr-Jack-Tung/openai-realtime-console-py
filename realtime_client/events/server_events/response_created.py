from typing import Literal

from pydantic import Field

from ...models import Response
from .base import ServerEvent


class ResponseCreated(ServerEvent):
    """Returned when a new Response is created.
    The first event of response creation, where the response is in an initial state of `in_progress`.
    """

    event_type: Literal["response.created"] = Field("response.created", alias="type")
    """The event type, must be 'response.created'."""

    response: Response
    """The response resource."""
