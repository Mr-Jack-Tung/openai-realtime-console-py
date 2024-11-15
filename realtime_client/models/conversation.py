from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


class Conversation(BaseModel):
    """A realtime Conversation represents an ongoing dialogue between a user and an AI assistant."""

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    """The unique ID of the conversation."""

    object_name: Literal["realtime.conversation"] = Field(
        "realtime.conversation", alias="object"
    )
    """The object type, must be "realtime.conversation"."""

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
