from pydantic import BaseModel, ConfigDict, Field


class ClientEvent(BaseModel):
    """The base client event class.

    Attributes:
        event_id (str | None): Optional client-generated ID used to identify this event.
    """

    model_config = ConfigDict(populate_by_name=True)

    event_id: str | None = Field(None)
    """Optional client-generated ID used to identify this event."""
