from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal

from .part import Part


class Item(BaseModel):
    """A realtime Item is of three types: `message`, `function_call`, or `function_call_output`.

    - A message item can contain text or audio.
    - A function_call item indicates a model's desire to call a tool.
    - A function_call_output item indicates a function response.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    """The unique ID of the item, this can be generated by the client to help manage server-side context, but is not required because the server will generate one if not provided."""

    object_name: Literal["realtime.item"] | None = Field(None, alias="object")
    """The object type, must be "realtime.item"."""

    item_type: Literal["message", "function_call", "function_call_output"] | None = (
        Field(None, alias="type")
    )
    """The type of the item (`message`, `function_call`, `function_call_output`)."""

    status: Literal["completed", "in_progress", "incomplete"] | None = None
    """The status of the item ("completed", "in_progress", "incomplete")."""

    role: Literal["user", "assistant", "system"] | None = None
    """The role of the message sender (`user`, `assistant`, `system`), only applicable for `message` items."""

    content: list[Part] | None = None
    """The content of the message, applicable for `message` items. 
    Message items with a role of `system` support only `input_text` content, message items of role `user` support `input_text` and `input_audio` content, and message items of role `assistant` support `text` content."""

    call_id: str | None = None
    """The ID of the function call (for `function_call` and `function_call_output` items). 
    If passed on a `function_call_output` item, the server will check that a `function_call` item with the same ID exists in the conversation history."""

    name: str | None = None
    """The name of the function being called (for `function_call` items)."""

    arguments: str | None = None
    """The arguments of the function call (for `function_call` items)."""

    output: str | None = None
    """The output of the function call (for `function_call_output` items)."""

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
