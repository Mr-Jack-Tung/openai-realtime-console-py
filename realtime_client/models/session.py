from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


class Session(BaseModel):
    """A session refers to a single WebSocket connection between a client and the server.

    Once a client creates a session, it then sends JSON-formatted events containing text and audio chunks.
    The server will respond in kind with audio containing voice output, a text transcript of that voice output, and function calls (if functions are provided by the client).

    A realtime Session represents the overall client-server interaction, and contains default configuration.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    """The unique ID of the session."""

    object_name: Literal["realtime.session"] | None = Field(None, alias="object")
    """The object type, must be "realtime.session"."""

    model: str | None = None
    """The default model used for this session."""

    modalities: list[str] | None = None
    """The set of modalities the model can respond with. To disable audio, set this to ["text"]."""

    instructions: str | None = None
    """The default system instructions (i.e. system message) prepended to model calls. 
    This field allows the client to guide the model on desired responses. 
    The model can be instructed on response content and format, (e.g. "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (e.g. "talk quickly", "inject emotion into your voice", "laugh frequently"). 
    The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.

    Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session.
    """

    voice: (
        Literal["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse"]
        | None
    ) = None
    """The voice the model uses to respond. 
    Supported voices are `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, and `verse`. 
    Cannot be changed once the model has responded with audio at least once.
    """

    input_audio_format: Literal["pcm16", "g711_ulaw", "g711_alaw"] | None = None
    """The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`."""

    output_audio_format: Literal["pcm16", "g711_ulaw", "g711_alaw"] | None = None
    """The format of output audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`."""

    input_audio_transcription: dict | None = None
    """Configuration for input audio transcription, defaults to off and can be set to `null` to turn off once on. 
    Input audio transcription is not native to the model, since the model consumes audio directly. 
    Transcription runs asynchronously through Whisper and should be treated as rough guidance rather than the representation understood by the model.
    """

    turn_detection: dict | None = None
    """Configuration for turn detection. 
    Can be set to `null` to turn off. 
    Server VAD means that the model will detect the start and end of speech based on audio volume and respond at the end of user speech.
    """

    tools: list[dict] | None = None
    """Tools (functions) available to the model."""

    tool_choice: Literal["auto", "none", "required"] | dict | None = None
    """How the model chooses tools. Options are `auto`, `none`, `required`, or specify a function."""

    temperature: float | None = None
    """Sampling temperature for the model, limited to [0.6, 1.2]. Defaults to 0.8."""

    max_response_output_tokens: int | Literal["inf"] | None = None
    """Maximum number of output tokens for a single assistant response, inclusive of tool calls. 
    Provide an integer between 1 and 4096 to limit output tokens, or `inf` for the maximum available tokens for a given model. 
    Defaults to `inf`.
    """

    def model_dump_json(self, **kwargs):
        self.object_name = "realtime.session"
        return super().model_dump_json(exclude_unset=True, by_alias=True, **kwargs)
