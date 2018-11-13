from cmd import Cmd
from logging import getLogger
from sparkbot.exceptions import CommandRunError
from types import GeneratorType

class ConsoleReceiver(Cmd):
    intro = "Welcome to the SparkBot-ng console receiver. Type 'help' or '?' to list commands.\n"
    prompt = "(sparkbot) "
    file = None

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.logger = getLogger("console_receiver")

    def do_command(self, arg):
        try:
            response = self.bot.command_dispatcher(arg)
        except CommandRunError as e:
            self.logger.exception(e)
            return

        if isinstance(response, GeneratorType):
            for token in response:
                print(token)
        else:
            print(response)
