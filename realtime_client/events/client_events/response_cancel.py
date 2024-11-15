from typing import Literal

from pydantic import Field

from .base import ClientEvent


class ResponseCancel(ClientEvent):
    """Send this event to cancel an in-progress response.
    The server will respond with a `response.cancelled` event or an error if there is no response to cancel.
    """

    event_type: Literal["response.cancel"] = Field("response.cancel", alias="type")
    """The event type, must be 'response.cancel'."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "response.cancel"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
