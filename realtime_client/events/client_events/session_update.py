from typing import Literal

from pydantic import Field

from ...models import SessionConfig
from .base import ClientEvent


class SessionUpdate(ClientEvent):
    """Send this event to update the session's default configuration.

    The client may send this event at any time to update the session configuration, and any field may be updated at any time, except for "voice".
    The server will respond with a session.updated event that shows the full effective configuration.
    Only fields that are present are updated, thus the correct way to clear a field like "instructions" is to pass an empty string.
    """

    event_type: Literal["session.update"] = Field("session.update", alias="type")
    """The event type, must be 'session.update'."""

    session: SessionConfig
    """Realtime session object configuration."""

    def dump_json(self, **kwargs):
        """Dump the event to a JSON string, used for sending to the OpenAI Realtime API"""
        self.event_type = "session.update"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
