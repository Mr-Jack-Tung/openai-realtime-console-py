from typing import Literal

from pydantic import Field

from ...models import Item
from .base import ServerEvent


class ResponseOutputItemDone(ServerEvent):
    """Returned when an Item is done streaming. Also emitted when a Response is interrupted, incomplete, or cancelled."""

    event_type: Literal["response.output_item.done"] = Field(
        "response.output_item.done", alias="type"
    )
    """The event type, must be 'response.output_item.done'."""

    response_id: str
    """The ID of the response to which the item belongs."""

    output_index: int
    """The index of the output item in the Response."""

    item: Item
    """The completed item."""
