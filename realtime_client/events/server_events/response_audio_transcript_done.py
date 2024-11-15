from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseAudioTranscriptDone(ServerEvent):
    """Returned when the model-generated transcription of audio output is done streaming.
    Also emitted when a Response is interrupted, incomplete, or cancelled.
    """

    event_type: Literal["response.audio_transcript.done"] = Field(
        "response.audio_transcript.done", alias="type"
    )
    """The event type, must be 'response.audio_transcript.done'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    transcript: str
    """The final transcript of the audio."""
