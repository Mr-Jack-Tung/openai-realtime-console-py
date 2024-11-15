from typing import Literal

from pydantic import Field

from ...models import Session
from .base import ServerEvent


class SessionUpdated(ServerEvent):
    """Returned when a session is updated with a `session.update` event, unless there is an error."""

    event_type: Literal["session.updated"] = Field("session.updated", alias="type")
    """The event type, must be 'session.updated'."""

    session: Session
    """Realtime session object configuration."""
