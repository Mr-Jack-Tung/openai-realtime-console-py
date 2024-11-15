from typing import Literal

from pydantic import Field

from .base import ServerEvent


class ConversationItemInputAudioTranscriptionCompleted(ServerEvent):
    """This event is the output of audio transcription for user audio written to the user audio buffer.
    Transcription begins when the input audio buffer is committed by the client or server (in `server_vad` mode).
    Transcription runs asynchronously with Response creation, so this event may come before or after the Response events.
    Realtime API models accept audio natively, and thus input transcription is a separate process run on a separate ASR (Automatic Speech Recognition) model, currently always `whisper-1`.
    Thus the transcript may diverge somewhat from the model's interpretation, and should be treated as a rough guide.
    """

    event_type: Literal["conversation.item.input_audio_transcription.completed"] = (
        Field("conversation.item.input_audio_transcription.completed", alias="type")
    )
    """The event type, must be 'conversation.item.input_audio_transcription.completed'."""

    item_id: str
    """The ID of the user message item containing the audio."""

    content_index: int
    """The index of the content part containing the audio."""

    transcript: str
    """The transcribed text."""
