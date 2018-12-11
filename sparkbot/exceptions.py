"""Exceptions thrown by sparkbot"""


class SparkBotError(Exception):
    """Generic exception"""


class CommandRunError(SparkBotError):
    """Raised when an issue is encountered during execution of a command"""


class CommandReturnError(CommandRunError):
    """Raised when a command does not return a str or GeneratorType"""


class CommandNotFound(CommandRunError):
    """Raised when a command is not found for the given request"""


class CommandStringError(CommandRunError):
    """Raised when the passed-in command string (user input) is invalid"""


class CommandSetupError(SparkBotError):
    """Raised when it is impossible to add the specified command for some reason.

    For example, this is raised when:

    * Attempting to add more than one fallback command
    * Attempting to add a non-fallback command with no command strings
    """
