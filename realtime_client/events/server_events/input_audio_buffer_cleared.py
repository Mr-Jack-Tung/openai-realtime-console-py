from typing import Literal

from pydantic import Field

from .base import ServerEvent


class InputAudioBufferCleared(ServerEvent):
    """Returned when the input audio buffer is cleared by the client with a `input_audio_buffer.clear` event."""

    event_type: Literal["input_audio_buffer.cleared"] = Field(
        "input_audio_buffer.cleared", alias="type"
    )
    """The event type, must be 'input_audio_buffer.cleared'."""
