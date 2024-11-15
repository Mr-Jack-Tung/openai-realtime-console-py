from typing import Literal

from pydantic import Field

from ...models.part import Part
from .base import ServerEvent


class ResponseContentPartAdded(ServerEvent):
    """Returned when a new content part is added to an assistant message item during response generation."""

    event_type: Literal["response.content_part.added"] = Field(
        "response.content_part.added", alias="type"
    )
    """The event type, must be 'response.content_part.added'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item to which the content part was added."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    part: Part
    """The content part that was added."""
