from typing import Literal

from pydantic import Field

from ...models import Item
from .base import ClientEvent


class ConversationItemCreate(ClientEvent):
    """Add a new Item to the Conversation's context, including messages, function calls, and function call responses.
    This event can be used both to populate a "history" of the conversation and to add new items mid-stream, but has the current limitation that it cannot populate assistant audio messages.
    If successful, the server will respond with a `conversation.item.created` event, otherwise an `error` event will be sent.
    """

    event_type: Literal["conversation.item.create"] = Field(
        "conversation.item.create", alias="type"
    )
    """The event type, must be 'conversation.item.create'."""

    previous_item_id: str | None = None
    """The ID of the preceding item after which the new item will be inserted.
    If not set, the new item will be appended to the end of the conversation.
    If set, it allows an item to be inserted mid-conversation. 
    If the ID cannot be found, an error will be returned and the item will not be added."""

    item: Item
    """The item to add to the conversation."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "conversation.item.create"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
