# Copyright 2018 Dalton Durst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .exceptions import (
    CommandNotFound,
    SparkBotError,
    CommandSetupError,
    CommandStringError,
    CommandRunError,
    CommandReturnError,
)
import logging
from types import FunctionType, GeneratorType
import textwrap
import shlex


class SparkBot:
    def __init__(self, logger=None):
        """ A simple Python chatbot

        SparkBot is a bot framework that focuses on being easy-to-use for developers.
        The SparkBot class is the bot itself, which takes string inputs and executes the
        functions specified.
        """

        self._logger = logging.getLogger(name="SparkBot")
        self.commands = {"help": self.my_help}
        self.fallback_command = self.my_fallback

        # The output of the "help all" command should only need to be determined once.
        # See self.my_help_all to learn more.
        self._help_all_string = ""

    """The output of :meth:`help_all`, generated once per run."""
    _help_all_string = ""

    def command(self, *args, fallback=False):
        """ Decorator that adds a command to this bot.

        :param args: Callable name(s) of command. When a bot user types this (these),
                     they call the decorated function. Pass a single string for a single
                     command name. Pass a list of strings to give a command multiple
                     names.
        :type args: str


        :param fallback: False by default, not required. If True, sets this command as a
                         "fallback command", used when the user requests a command that does not
                         exist.
        :type fallback: bool

        :raises CommandSetupError: Arguments or combination of arguments was incorrect.
                                   The error description will have more details.

        :raises TypeError: Type of arguments was incorrect.
        """

        if len(args) == 0 and not fallback:
            raise CommandSetupError(
                "Command strings not given in call to SparkBot.command() and fallback not set."
            )
        elif not fallback and isinstance(args[0], FunctionType):
            raise CommandSetupError(
                "command_strings not given in call to SparkBot.command. Did you include the parentheses in your decorator?"
            )

        def decorator(function):

            if not isinstance(fallback, bool):
                raise TypeError("fallback not a boolean in call to SparkBot.command.")

            new_command = function

            # Register new command object under each of its names
            if fallback:
                if self.fallback_command != self.my_fallback:
                    # There is already a custom fallback command
                    raise CommandSetupError(
                        "Attempted to add a fallback command twice on one bot instance."
                    )

                self.fallback_command = new_command
            else:
                for command in args:
                    if not isinstance(command, str):
                        raise TypeError("non-str object found in command strings.")

                    self.commands[command] = new_command

            return function

        return decorator

    def command_dispatcher(self, user_message):
        """ Dispatches a command for ``user_message``

        :param user_message: The text of the message sent by the user when calling the
                             bot. The first token of this message must be the command
                             the user wishes to call, ensure that you have properly
                             sanitized the string before calling.

        :raises CommandNotFound: The command requested by the user does not exist and
                                 no fallback command has been set.

        :returns: GeneratorType or str, depending on the called command.

        See (TODO:link "dispatching commands" section of receiver API doc) to learn more
        about dispatching commands as a receiver developer.
        """

        # Catch any errors in the shlex string
        try:
            commandline = shlex.split(user_message)
        except ValueError:
            # Something is incorrect in the user's command string
            raise CommandStringError()

        user_requested_function = str.lower(commandline[0])

        if user_requested_function in self.commands:
            command_to_run = self.commands[user_requested_function]
        elif self.fallback_command:
            command_to_run = self.fallback_command
        else:
            raise CommandNotFound()

        try:
            command_response = command_to_run(commandline)
        except Exception as e:
            self._logger.exception(e)
            raise CommandRunError("Command raised an exception. See log for more details.")

        if isinstance(command_response, str) or isinstance(command_response, GeneratorType):
            return command_response
        else:
            raise CommandReturnError("Command did not return a str or GeneratorType.")

    def my_help(self, commandline):
        """
        The default help command.

        Usage: `help [command]`

        Gives the help for [command]. If a command is not given (or is `all`), gives `help-all`.
        """

        try:
            command_to_help = commandline[1]
        except IndexError:
            # The user did not specify a command to get help on. Return the "help-all" command.
            return self.my_help_all()

        if str.lower(command_to_help) == "all":
            return self.my_help_all()

        try:
            help_text_raw = self.commands[command_to_help].__doc__
            help_text = textwrap.dedent(help_text_raw)
        except KeyError:
            # The requested command doesn't exist
            help_text = 'I don\'t have a command with the name "{}".'.format(
                command_to_help
            )
        except TypeError:
            # The requested command doesn't have a docstring
            help_text = "There is no help available for `{}`.".format(command_to_help)

        return help_text

    def my_help_all(self):
        """Returns a formatted list of all commands for this bot"""

        # Create a formatted string containing all of our commands
        # One command can have multiple names and therefore takes up multiple slots in the
        # self.commands dict. However, for this help, we want multiple names for one command
        # to be grouped together. In this process, we'll look at every command added to this bot
        # and group together ones which are the same.
        # We can't add or remove commands after the bot starts, so we can create this string once
        if not self._help_all_string:
            temp_command_list = []
            used_command_string_list = []

            # Iterate over all of our commands to obtain a list where multiple
            # names for one command are in the same entry.
            for command_string, command_object in self.commands.items():

                if command_string in used_command_string_list:
                    continue

                used_command_string_list.append(command_string)
                current_command_strings = [command_string]

                # Iterate over the commands *again* and put any names for commands that
                # match the one we're currently checking into current_command_strings
                for inner_command_string, inner_command_object in self.commands.items():
                    if (
                        inner_command_object == command_object
                        and command_string != inner_command_string
                    ):
                        used_command_string_list.append(inner_command_string)
                        current_command_strings.append(inner_command_string)

                temp_command_list.append(", ".join(sorted(current_command_strings)))

            sorted_commands = sorted(temp_command_list)

            output = (
                "Type `help [command]` for more specific help about any of these commands:\n - "
                + "\n - ".join(sorted_commands)
            )

            self._help_all_string = output

        return self._help_all_string

    def my_fallback(self, commandline):
        """The default "fallback" command

        This function is dispatched when the user types a command that doesn't exist.
        It can be replaced by adding a new command with the ``fallback`` argument set
        to ``True``.
        """

        return "Command not found. Maybe try 'help'?"
