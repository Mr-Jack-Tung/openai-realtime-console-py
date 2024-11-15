from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseAudioDelta(ServerEvent):
    """Returned when the model-generated audio is updated."""

    event_type: Literal["response.audio.delta"] = Field(
        "response.audio.delta", alias="type"
    )
    """The event type, must be 'response.audio.delta'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    delta: str
    """Base64-encoded audio data delta."""
