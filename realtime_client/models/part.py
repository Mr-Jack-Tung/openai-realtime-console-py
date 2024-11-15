from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


class Part(BaseModel):
    """A part of a conversation item."""

    model_config = ConfigDict(populate_by_name=True)

    part_type: Literal["text", "audio", "input_text", "input_audio"] | None = Field(
        None, alias="type"
    )
    """The content type (`text`, `audio`, `input_text`, `input_audio`)."""

    text: str | None = None
    """The `text` content, used for `input_text` and `text` content types."""

    audio: str | None = None
    """Base64-encoded audio bytes, used for `input_audio` and `audio` content type."""

    transcript: str | None = None
    """The transcript of the audio, used for `input_audio` and `audio` content type."""

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
