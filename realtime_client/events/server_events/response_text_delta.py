from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseTextDelta(ServerEvent):
    """Returned when the text value of a "text" content part is updated."""

    event_type: Literal["response.text.delta"] = Field(
        "response.text.delta", alias="type"
    )
    """The event type, must be 'response.text.delta'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    delta: str
    """The text delta."""
