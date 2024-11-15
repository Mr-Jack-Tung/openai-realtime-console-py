from typing import Literal

from pydantic import Field

from .base import ClientEvent


class InputAudioBufferCommit(ClientEvent):
    """Send this event to commit the user input audio buffer, which will create a new user message item in the conversation.
    This event will produce an error if the input audio buffer is empty.
    When in Server VAD mode, the client does not need to send this event, the server will commit the audio buffer automatically.
    Committing the input audio buffer will trigger input audio transcription (if enabled in session configuration), but it will not create a response from the model.
    The server will respond with an `input_audio_buffer.committed` event.
    """

    event_type: Literal["input_audio_buffer.commit"] = Field(
        "input_audio_buffer.commit", alias="type"
    )
    """The event type, must be 'input_audio_buffer.commit'."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "input_audio_buffer.commit"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
