from typing import Literal

from pydantic import Field

from .base import ServerEvent


class InputAudioBufferCommitted(ServerEvent):
    """Returned when an input audio buffer is committed, either by the client or automatically in server VAD mode.
    The `item_id` property is the ID of the user message item that will be created, thus a `conversation.item.created` event will also be sent to the client.
    """

    event_type: Literal["input_audio_buffer.committed"] = Field(
        "input_audio_buffer.committed", alias="type"
    )
    """The event type, must be 'input_audio_buffer.committed'."""

    previous_item_id: str
    """The ID of the preceding item after which the new item will be inserted."""

    item_id: str
    """The ID of the user message item that will be created."""
