from typing import Literal

from pydantic import Field

from .base import ServerEvent


class InputAudioBufferSpeechStopped(ServerEvent):
    """Returned in `server_vad` mode when the server detects the end of speech in the audio buffer.
    The server will also send an `conversation.item.created` event with the user message item that is created from the audio buffer.
    """

    event_type: Literal["input_audio_buffer.speech_stopped"] = Field(
        "input_audio_buffer.speech_stopped", alias="type"
    )
    """The event type, must be 'input_audio_buffer.speech_stopped'."""

    audio_end_ms: int
    """Milliseconds since the session started when speech stopped. 
    This will correspond to the end of audio sent to the model, and thus includes the `min_silence_duration_ms` configured in the Session."""

    item_id: str
    """The ID of the user message item that will be created."""
