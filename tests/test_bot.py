import pytest
from sparkbot import SparkBot
from sparkbot.exceptions import CommandNotFound, CommandSetupError


class TestBot:
    """Collection of tests for sparkbot.SparkBot"""

    @pytest.fixture
    def bot(self):
        return SparkBot()

    def test_add_command(self):
        """Tests that the bot will add a command"""

        bot = SparkBot()

        @bot.command("command")
        def ping():
            pass

        assert bot.commands["command"] is ping

    def test_bad_decorator_call(self, bot):
        """Tests that the bot will fail to add a command when command() is called with no arguments"""

        with pytest.raises(CommandSetupError):

            @bot.command
            def ping():
                pass

    def test_bad_decorator_type(self, bot):
        """Tests that the bot will fail to add a command with the incorrect argument type"""

        with pytest.raises(TypeError):

            @bot.command(bot)
            def ping(bot):
                pass

    def test_bad_decorator_embedded_type(self, bot):
        """
        Tests that the bot will fail to add a command with the incorrect argument type
        """

        with pytest.raises(TypeError):

            @bot.command([bot, "stuff"])
            def ping():
                pass

    def test_fallback_failure_on_multiple(self, bot):
        """Tests that trying to set more than one fallback command fails"""

        @bot.command(fallback=True)
        def fallback():
            pass

        with pytest.raises(CommandSetupError):

            @bot.command(fallback=True)
            def second_fallback():
                pass

    def test_add_command_multiple_strings(self, bot):
        """Tests adding a command with multiple command strings"""

        @bot.command("one", "two")
        def ping():
            pass

        assert bot.commands["one"] is ping
        assert bot.commands["two"] is ping

    def test_help(self, bot):
        """Tests the default help command"""

        @bot.command("help-command")
        def help_command():
            """I am help"""
            pass

        assert bot.my_help(["help", "help-command"]) == "I am help"

    def test_help_blank(self, bot):
        """Tests the default help command when the command has no help"""

        @bot.command("help-command")
        def help_command():
            pass

        assert (
            bot.my_help(["help", "help-command"])
            == "There is no help available for `help-command`."
        )

    def test_help_all(self, bot):
        """Tests the default help all command"""

        @bot.command("help-command")
        def help_command():
            pass

        @bot.command("help-command-one", "help-command-two")
        def other_help_command():
            pass

        assert (
            bot.my_help_all()
            == """Type `help [command]` for more specific help about any of these commands:
 - help
 - help-command
 - help-command-one, help-command-two"""
        )

    def test_help_adding(self, bot):
        """Tests that my_help is added as the command for 'help'"""

        assert bot.commands["help"] == bot.my_help
