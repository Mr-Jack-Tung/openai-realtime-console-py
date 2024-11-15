from typing import Literal

from pydantic import Field

from ...models import Session
from .base import ServerEvent


class SessionCreated(ServerEvent):
    """Returned when a Session is created.
    Emitted automatically when a new connection is established as the first server event.
    This event will contain the default Session configuration.
    """

    event_type: Literal["session.created"] = Field("session.created", alias="type")
    """The event type, must be 'session.created'."""

    session: Session
    """The session resource."""
