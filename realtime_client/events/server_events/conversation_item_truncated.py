from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ConversationItemTruncated(ServerEvent):
    """Returned when an earlier assistant audio message item is truncated by the client with a `conversation.item.truncate` event.
    This event is used to synchronize the server's understanding of the audio with the client's playback.
    This action will truncate the audio and remove the server-side text transcript to ensure there is no text in the context that hasn't been heard by the user.
    """

    event_type: Literal["conversation.item.truncated"] = Field(
        "conversation.item.truncated", alias="type"
    )
    """The event type, must be 'conversation.item.truncated'."""

    item_id: str
    """The ID of the assistant message item that was truncated."""

    context_index: int
    """The index of the content part that was truncated."""

    audio_end_ms: int
    """The duration up to which the audio was truncated, in milliseconds."""
