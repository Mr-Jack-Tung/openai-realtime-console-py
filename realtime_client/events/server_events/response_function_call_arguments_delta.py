from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ResponseFunctionCallArgumentsDelta(ServerEvent):
    """Returned when the model-generated function call arguments are updated."""

    event_type: Literal["response.function_call_arguments.delta"] = Field(
        "response.function_call_arguments.delta", alias="type"
    )
    """The event type, must be 'response.function_call_arguments.delta'."""

    response_id: str
    """The ID of the response."""

    item_id: str
    """The ID of the function call item."""

    output_index: int
    """The index of the output item in the response."""

    call_id: str
    """The ID of the function call."""

    delta: str
    """The arguments delta as a JSON string."""
