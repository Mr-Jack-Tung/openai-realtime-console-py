from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseFunctionCallArgumentsDone(ServerEvent):
    """Returned when the model-generated function call arguments are done streaming.
    Also emitted when a Response is interrupted, incomplete, or cancelled.
    """

    event_type: Literal["response.function_call_arguments.done"] = Field(
        "response.function_call_arguments.done", alias="type"
    )
    """The event type, must be 'response.function_call_arguments.done'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the function call item."""

    output_index: int
    """The index of the output item in the response."""

    call_id: str
    """The ID of the function call."""

    arguments: str
    """The final arguments as a JSON string."""
