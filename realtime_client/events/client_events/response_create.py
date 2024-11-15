from typing import Literal

from pydantic import Field

from ...models import ResponseConfig
from .base import ClientEvent


class ResponseCreate(ClientEvent):
    """This event instructs the server to create a Response, which means triggering model inference.
    When in Server VAD mode, the server will create Responses automatically.
    A Response will include at least one Item, and may have two, in which case the second will be a function call.
    These Items will be appended to the conversation history.
    The server will respond with a `response.created` event, events for Items and content created, and finally a `response.done` event to indicate the Response is complete.
    The `response.create` event includes inference configuration like `instructions`, and `temperature`.
    These fields will override the Session's configuration for this Response only.
    """

    event_type: Literal["response.create"] = Field("response.create", alias="type")
    """The event type, must be 'response.create'."""

    response: ResponseConfig | None = None
    """Configuration for the response."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "response.create"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
