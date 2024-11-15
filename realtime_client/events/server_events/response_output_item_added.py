from typing import Literal

from pydantic import Field

from ...models import Item
from .base import ServerEvent


class ResponseOutputItemAdded(ServerEvent):
    """Returned when a new Item is created during response generation."""

    event_type: Literal["response.output_item.added"] = Field(
        "response.output_item.added", alias="type"
    )
    """The event type, must be 'response.output_item.added'."""

    response_id: str
    """The ID of the response to which the item belongs."""

    output_index: int
    """The index of the output item in the response."""

    item: Item
    """The item that was added."""
