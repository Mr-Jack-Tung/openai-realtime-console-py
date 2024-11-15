from typing import Literal

from pydantic import Field

from .base import ClientEvent


class ConversationItemDelete(ClientEvent):
    """Send this event when you want to remove any item from the conversation history.
    The server will respond with a `conversation.item.deleted` event,
    unless the item does not exist in the conversation history, in which case the server will respond with an error.
    """

    event_type: Literal["conversation.item.delete"] = Field(
        "conversation.item.delete", alias="type"
    )
    """The event type, must be 'conversation.item.delete'."""

    item_id: str
    """The ID of the item to delete."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "conversation.item.delete"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
