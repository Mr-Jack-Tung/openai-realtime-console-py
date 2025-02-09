from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal

from .item import Item


class Response(BaseModel):
    """A response model representing the output from the server."""

    model_config = ConfigDict(populate_by_name=True)

    id: str | None
    """The unique ID of the response."""

    object_name: Literal["realtime.response"] | None = Field(None, alias="object")
    """The object type, must be "realtime.response"."""

    status: (
        Literal["in_progress", "completed", "cancelled", "failed", "incomplete"] | None
    ) = None
    """The status of the response."""

    status_details: dict | None = None
    """Additional details about the status."""

    output: list[Item] | None = None
    """The list of output items generated by the response."""

    usage: dict | None = None
    """Usage statistics for the Response, this will correspond to billing. 
    A Realtime API session will maintain a conversation context and append new Items to the Conversation, thus output from previous turns (text and audio tokens) will become the input for later turns."""

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
