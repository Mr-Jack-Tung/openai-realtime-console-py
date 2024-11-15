from typing import Literal

from pydantic import Field

from ...models import Response
from .base import ServerEvent


class ResponseDone(ServerEvent):
    """Returned when a Response is done streaming.
    Always emitted, no matter the final state.
    The Response object included in the `response.done` event will include all output Items in the Response but will omit the raw audio data.
    """

    event_type: Literal["response.done"] = Field("response.done", alias="type")
    """The event type, must be 'response.done'."""

    response: Response
    """The response resource."""
