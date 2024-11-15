from typing import Literal

from pydantic import Field

from ...models import Conversation
from .base import ServerEvent


class ConversationCreated(ServerEvent):
    """Returned when a conversation is created. Emitted right after session creation."""

    event_type: Literal["conversation.created"] = Field(
        "conversation.created", alias="type"
    )
    """The event type, must be 'conversation.created'."""

    conversation: Conversation
    """The conversation resource."""
