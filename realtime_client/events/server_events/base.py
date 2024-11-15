from pydantic import BaseModel, ConfigDict


class ServerEvent(BaseModel):
    """The base server event class.

    Attributes:
        event_id (str): The unique ID of the server event.
    """

    model_config = ConfigDict(populate_by_name=True)

    event_id: str
    """The unique ID of the server event."""
