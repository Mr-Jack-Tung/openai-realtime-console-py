import asyncio
import inspect
import json
import os
from types import TracebackType

from typing_extensions import Any, Awaitable, Callable, Self, TypedDict
from websockets import ConnectionClosed, ConnectionClosedError, connect
from websockets.client import ClientConnection
from websockets.protocol import State

from .events import (
    ConversationItemCreate,
    ConversationItemDelete,
    ConversationItemTruncate,
    InputAudioBufferAppend,
    InputAudioBufferClear,
    InputAudioBufferCommit,
    RealtimeClientEvent,
    ResponseCancel,
    ResponseCreate,
    ServerEventName,
    SessionUpdate,
)
from .models import Item, ResponseConfig, SessionConfig
from .utils import background_task, get_logger
from .utils.logger import RealtimeClientLogger

EventHandlerCallable = (
    Callable[[dict, tuple, dict], Any] | Callable[[dict, tuple, dict], Awaitable[Any]]
)


class EventHandlerType(TypedDict):
    handler: EventHandlerCallable
    args: tuple
    kwargs: dict


class RealtimeClient:
    """A client for interacting with OpenAI's Realtime API.

    This client provides asynchronous methods for communication with OpenAI's Realtime API,
    using an event-based architecture.

    Args:
        uri (str): WebSocket endpoint URI. Defaults to `'wss://api.openai.com/v1/realtime'`.
        model_name (str): OpenAI model identifier. Defaults to `'gpt-4o-realtime-preview-2024-10-01'`.
        api_key (str | None): OpenAI API key. If `None`, reads from OPENAI_API_KEY environment variable.

    Example:
        ```python
        >>> from realtime_client import RealtimeClient
        >>> from realtime_client.models import SessionConfig
        >>>
        >>> async with RealtimeClient() as client:
        >>>    # Add event handlers
        >>>    client.on("response.text.delta", handle_text_delta)
        >>>
        >>>    # Configure session
        >>>    await client.session_update(
        >>>        SessionConfig(
        >>>            modalities=["text"],
        >>>            temperature=0.9,
        >>>            input_audio_transcription=None,
        >>>            turn_detection=None,
        >>>        )
        >>>    )
        >>>    await client.wait_for("session.updated")
        ```

    Note:
        It is recommended to use the client as an async context manager to ensure proper
        connection handling and cleanup of resources.
    """

    def __init__(
        self,
        uri: str = "wss://api.openai.com/v1/realtime",
        model_name: str = "gpt-4o-realtime-preview-2024-10-01",
        api_key: str | None = None,
    ):
        self.uri: str = uri
        self.model_name: str = model_name or "gpt-4o-realtime-preview-2024-10-01"
        self.api_key: str | None = api_key or os.environ.get("OPENAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in OPENAI_API_KEY environment variable"
            )
        self.ws: ClientConnection | None = None
        self.event_handlers: dict[ServerEventName, EventHandlerType] = {}
        self.pending_events: dict[ServerEventName, asyncio.Event] = {}
        self.logger: RealtimeClientLogger = get_logger()
        self.listener_task: asyncio.Task | None = None

    async def __aenter__(self) -> Self:
        await self.connect()
        self.listener_task = asyncio.create_task(self.listener())
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        self.event_handlers.clear()
        self.pending_events.clear()
        self.listener_task.cancel()
        self.listener_task = None
        await self.disconnect()

    @background_task
    async def listener(self) -> None:
        """Background task that listens for incoming websocket messages.

        Continuously receives messages from the websocket connection, parses them as JSON events,
        and emits them to any registered handlers. Will cancel itself if the connection is closed
        or an error occurs.
        """
        try:
            async for message in self.ws:
                event = json.loads(message)
                await self.emit(event["type"], event)
        except (ConnectionClosedError, ConnectionClosed):
            self.logger.error("Websocket connection closed")
            self.listener_task.cancel()
        except Exception as e:
            self.logger.error(f"Event handler error for {event['type']}: {e}")
            self.listener_task.cancel()

    def on(
        self,
        event_name: ServerEventName,
        handler: EventHandlerCallable,
        *args,
        **kwargs,
    ) -> None:
        """Register an event handler for a server event.

        The handler can be either a normal function or an async function. When the event occurs,
        the handler will be called with:
        - The event payload as the first argument
        - Any additional *args and **kwargs passed during registration

        Args:
            event_name: The server event name to listen for
            handler: The function or coroutine to call when the event occurs
            *args: Additional positional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self.event_handlers[event_name] = {
            "handler": handler,
            "args": args,
            "kwargs": kwargs,
        }

    def off(self, event_name: ServerEventName) -> None:
        """Delete the event handler for a server event.

        Args:
            event_name: The server event name to stop listening for
        """
        if event_name in self.event_handlers:
            del self.event_handlers[event_name]

    async def emit(self, event_name: ServerEventName, event: dict) -> None:
        """Emit an event to registered handlers and resolve pending `wait_for()` calls.

        Args:
            event_name: The server event name that was received
            event: The event payload dictionary containing event data
        """
        self.logger.log_event(event, "server")
        # WARNING: this will run user code in a background task, if any exceptions occur, it will be eaten
        if event_name in self.pending_events:
            self.pending_events[event_name].set()
        if event_name in self.event_handlers:
            handler_info = self.event_handlers[event_name]
            if inspect.iscoroutinefunction(handler_info["handler"]):
                await handler_info["handler"](
                    event, *handler_info["args"], **handler_info["kwargs"]
                )
            else:
                handler_info["handler"](
                    event, *handler_info["args"], **handler_info["kwargs"]
                )

    def is_connected(self) -> bool:
        """Check if the websocket connection is currently active and open.

        Returns:
            bool: True if connected and open, False otherwise
        """
        return self.ws is not None and self.ws.state == State.OPEN

    async def connect(self) -> None:
        """Connect to the realtime websocket server.

        Raises:
            ValueError: If already connected to websocket
        """
        full_uri = f"{self.uri}?model={self.model_name}"
        if not self.is_connected():
            self.ws = await connect(
                full_uri,
                additional_headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "OpenAI-Beta": "realtime=v1",
                },
                close_timeout=30,
                ping_timeout=30,
                open_timeout=60,
                ping_interval=30,
            )
            self.logger.debug(f"Connected to {self.uri}")
        else:
            raise ValueError("Already connected to websocket")

    async def disconnect(self) -> None:
        """Disconnect from the realtime websocket server.

        Raises:
            ValueError: If not currently connected to websocket
        """
        if self.is_connected():
            await self.ws.close()
            self.logger.debug(f"Disconnected from {self.uri}")
        else:
            raise ValueError("Not connected to websocket")

    async def send_event(self, event: RealtimeClientEvent) -> None:
        """Send an event to the realtime websocket server.

        Args:
            event: The event to send

        Raises:
            ConnectionError: If not connected to websocket
        """
        if self.is_connected():
            self.logger.log_event(json.loads(event.dump_json()), "client")
            await self.ws.send(event.dump_json())
        else:
            raise ConnectionError("Not connected to websocket")

    async def wait_for(
        self, event_name: ServerEventName, timeout: float | None = None
    ) -> None:
        """Wait for a specific server event to occur.

        Args:
            event_name: The name of the server event to wait for
            timeout: Optional timeout in seconds. If None, wait indefinitely

        Raises:
            asyncio.TimeoutError: If timeout is reached before event occurs
        """
        if event_name not in self.pending_events:
            self.pending_events[event_name] = asyncio.Event()
            await asyncio.wait_for(self.pending_events[event_name].wait(), timeout)
            del self.pending_events[event_name]

    # High-level event helpers ==================================================

    async def conversation_item_create(self, item: Item) -> None:
        """Send a `conversation.item.create` event to the Realtime API server.

        Args:
            item: The conversation item to create

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(ConversationItemCreate(item=item))

    async def conversation_item_delete(self, item_id: str) -> None:
        """Send a `conversation.item.delete` event to the Realtime API server.

        Args:
            item_id: The ID of the conversation item to delete

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(ConversationItemDelete(item_id=item_id))

    async def conversation_item_truncate(
        self, item_id: str, content_index: int, audio_end_ms: int
    ) -> None:
        """Send a `conversation.item.truncate` event to the Realtime API server.

        Args:
            item_id: The ID of the conversation item to truncate
            content_index: The index of the content part to truncate. Set this to 0.
            audio_end_ms: Inclusive duration up to which audio is truncated, in milliseconds. If the audio_end_ms is greater than the actual audio duration, the server will respond with an error.

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(
            ConversationItemTruncate(
                item_id=item_id,
                content_index=content_index,
                audio_end_ms=audio_end_ms,
            )
        )

    async def input_audio_buffer_append(self, audio_bytes: str) -> None:
        """Send an `input.audio.buffer.append` event to the Realtime API server.

        Args:
            audio_bytes: The Base64 encoded audio bytes to append to the input buffer

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(InputAudioBufferAppend(audio=audio_bytes))

    async def input_audio_buffer_clear(self) -> None:
        """Send an `input.audio.buffer.clear` event to the Realtime API server.

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(InputAudioBufferClear())

    async def input_audio_buffer_commit(self) -> None:
        """Send an `input.audio.buffer.commit` event to the Realtime API server.

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(InputAudioBufferCommit())

    async def response_cancel(self) -> None:
        """Send a `response.cancel` event to the Realtime API server.

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(ResponseCancel())

    async def response_create(
        self, response_config: ResponseConfig | None = None
    ) -> None:
        """Send a `response.create` event to the Realtime API server.

        Args:
            response_config: Optional configuration for the response

        Raises:
            ConnectionError: If not connected to websocket
        """
        if response_config:
            await self.send_event(ResponseCreate(response=response_config))
        else:
            await self.send_event(ResponseCreate())

    async def session_update(self, session_config: SessionConfig) -> None:
        """Send a `session.update` event to the Realtime API server.

        Args:
            session_config: Configuration for the session update

        Raises:
            ConnectionError: If not connected to websocket
        """
        await self.send_event(SessionUpdate(session=session_config))
