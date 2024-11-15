from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseTextDone(ServerEvent):
    """Returned when the text value of a "text" content part is done streaming.
    Also emitted when a Response is interrupted, incomplete, or cancelled.
    """

    event_type: Literal["response.text.done"] = Field(
        "response.text.done", alias="type"
    )
    """The event type, must be 'response.text.done'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    text: str
    """The final text content."""
