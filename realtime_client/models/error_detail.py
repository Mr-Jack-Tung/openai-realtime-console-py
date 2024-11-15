from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Represents details of an error."""

    model_config = ConfigDict(populate_by_name=True)

    error_type: str | None = Field(None, alias="type")
    """The type of error (e.g., "invalid_request_error", "server_error"). Alias: "type"."""

    code: str | None = None
    """Error code, if any."""

    message: str | None = None
    """A human-readable error message."""

    param: str | None = None
    """Parameter related to the error, if any."""

    event_id: str | None = None
    """The event_id of the client event that caused the error, if applicable."""

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
