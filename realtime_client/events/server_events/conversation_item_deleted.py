from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ConversationItemDeleted(ServerEvent):
    """Returned when an item in the conversation is deleted by the client with a `conversation.item.delete` event.
    This event is used to synchronize the server's understanding of the conversation history with the client's view.
    """

    event_type: Literal["conversation.item.deleted"] = Field(
        "conversation.item.deleted", alias="type"
    )
    """The event type, must be 'conversation.item.deleted'."""

    item_id: str
    """The ID of the item that was deleted."""
