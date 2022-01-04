from discord.ext import commands
from inspect import Parameter

__all__ = (
    'VoiceConnectionError',
    'InvalidVoiceChannel',
    'EmptyQueue'
)

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

class EmptyQueue(commands.CommandError):
    """Because queue was empty"""

class MissingRequiredArgument(commands.UserInputError):
    """Exception raised when parsing a command and a parameter
    that is required is not encountered.
    This inherits from :exc:`UserInputError`
    Attributes
    -----------
    param: :class:`inspect.Parameter`
        The argument that is missing.
    """
    def __init__(self, param: Parameter) -> None:
        self.param: Parameter = param
        super().__init__(param.name)