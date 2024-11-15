from typing import Literal

from pydantic import Field

from .base import ServerEvent


class InputAudioBufferSpeechStarted(ServerEvent):
    """Sent by the server when in `server_vad` mode to indicate that speech has been detected in the audio buffer.
    This can happen any time audio is added to the buffer (unless speech is already detected).
    The client may want to use this event to interrupt audio playback or provide visual feedback to the user.
    The client should expect to receive a `input_audio_buffer.speech_stopped` event when speech stops.
    The `item_id` property is the ID of the user message item that will be created when speech stops and will also be included in the `input_audio_buffer.speech_stopped` event (unless the client manually commits the audio buffer during VAD activation).
    """

    event_type: Literal["input_audio_buffer.speech_started"] = Field(
        "input_audio_buffer.speech_started", alias="type"
    )
    """The event type, must be 'input_audio_buffer.speech_started'."""

    audio_start_ms: int
    """Milliseconds from the start of all audio written to the buffer during the session when speech was first detected. 
    This will correspond to the beginning of audio sent to the model, and thus includes the `prefix_padding_ms` configured in the Session."""

    item_id: str
    """The ID of the user message item that will be created when speech stops."""
