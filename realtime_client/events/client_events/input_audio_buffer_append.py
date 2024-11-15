from typing import Literal

from pydantic import Field

from .base import ClientEvent


class InputAudioBufferAppend(ClientEvent):
    """Send this event to append audio bytes to the input audio buffer.
    The audio buffer is temporary storage you can write to and later commit.
    In Server VAD mode, the audio buffer is used to detect speech and the server will decide when to commit.
    When Server VAD is disabled, you must commit the audio buffer manually.
    The client may choose how much audio to place in each event up to a maximum of 15 MiB, for example streaming smaller chunks from the client may allow the VAD to be more responsive.
    Unlike other client events, the server will not send a confirmation response to this event.
    """

    event_type: Literal["input_audio_buffer.append"] = Field(
        "input_audio_buffer.append", alias="type"
    )
    """The event type, must be 'input_audio_buffer.append'."""

    audio: str
    """Base64-encoded audio bytes. This must be in the format specified by the `input_audio_format` field in the session configuration."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "input_audio_buffer.append"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
