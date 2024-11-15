from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseAudioDone(ServerEvent):
    """Returned when the model-generated audio is done. Also emitted when a Response is interrupted, incomplete, or cancelled."""

    event_type: Literal["response.audio.done"] = Field(
        "response.audio.done", alias="type"
    )
    """The event type, must be 'response.audio.done'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""
