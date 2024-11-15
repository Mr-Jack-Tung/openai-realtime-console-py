from typing import Literal

from pydantic import Field

from ...models import ErrorDetail
from .base import ServerEvent


class ConversationItemInputAudioTranscriptionFailed(ServerEvent):
    """Returned when input audio transcription is configured, and a transcription request for a user message failed.
    These events are separate from other `error` events so that the client can identify the related Item.
    """

    event_type: Literal["conversation.item.input_audio_transcription.failed"] = Field(
        "conversation.item.input_audio_transcription.failed", alias="type"
    )
    """The event type, must be 'conversation.item.input_audio_transcription.failed'."""

    item_id: str
    """The ID of the user message item."""

    content_index: int
    """The index of the content part containing the audio."""

    error: ErrorDetail
    """Details of the transcription error."""
