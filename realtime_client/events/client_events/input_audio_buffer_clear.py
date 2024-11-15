from typing import Literal

from pydantic import Field

from .base import ClientEvent


class InputAudioBufferClear(ClientEvent):
    """Send this event to clear the audio bytes in the buffer. The server will respond with an `input_audio_buffer.cleared` event."""

    event_type: Literal["input_audio_buffer.clear"] = Field(
        "input_audio_buffer.clear", alias="type"
    )
    """The event type, must be 'input_audio_buffer.clear'."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "input_audio_buffer.clear"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
