from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseAudioTranscriptDelta(ServerEvent):
    """Returned when the model-generated transcription of audio output is updated."""

    event_type: Literal["response.audio_transcript.delta"] = Field(
        "response.audio_transcript.delta", alias="type"
    )
    """The event type, must be 'response.audio_transcript.delta'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    content_index: int
    """The index of the content part in the item's content array."""

    delta: str
    """The transcript delta."""
