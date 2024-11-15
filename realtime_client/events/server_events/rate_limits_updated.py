from typing import Literal

from pydantic import Field

from .base import ServerEvent


class RateLimitsUpdated(ServerEvent):
    """Emitted at the beginning of a Response to indicate the updated rate limits.
    When a Response is created some tokens will be "reserved" for the output tokens, the rate limits shown here reflect that reservation, which is then adjusted accordingly once the Response is completed.
    """

    event_type: Literal["rate_limits.updated"] = Field(
        "rate_limits.updated", alias="type"
    )
    """The event type, must be 'rate_limits.updated'."""

    rate_limits: list[dict]
    """List of rate limit information."""
