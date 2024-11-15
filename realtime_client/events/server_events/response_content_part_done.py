from typing import Literal

from pydantic import Field

from ...models.part import Part
from .base import ServerEvent


class ResponseContentPartDone(ServerEvent):
    """Returned when a content part is done streaming in an assistant message item.
    Also emitted when a Response is interrupted, incomplete, or cancelled.
    """

    event_type: Literal["response.content_part.done"] = Field(
        "response.content_part.done", alias="type"
    )
    """The event type, must be 'response.content_part.done'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    part: Part
    """The content part that is done."""
