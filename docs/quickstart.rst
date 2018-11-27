Quickstart
==========

This document will lead you through the steps to run Sparkbot on your development machine and write basic commands.

Dependencies
------------

First you'll need to install the prerequisites for running SparkBot.

SparkBot requires the following software:

* Python 3.6 or higher with Pip

To get started, we'll need to install ``virtualenv`` which we'll use to keep SparkBot's dependencies from cluttering the rest of the system. Run the following command to install it::

    pip3 install virtualenv --user

Set up your virtualenv
----------------------

With virtualenv installed, we can set up an environment where all of the SparkBot dependencies can be installed without touching any of the system packages. Let's start by creating a new virtualenv in your home folder::

    python3 -m virtualenv --python=python3 ~/sparkbotenv

Whenever you'd like to use the virtualenv, you can activate it::

    # Linux
    source ~/sparkbotenv/bin/activate

    # Windows (Powershell)
    ~/sparkbotenv/Scripts/activate.ps1

SparkBot's dependencies are automatically installed with it, so we'll install the base version now::

    pip install git+https://github.com/UniversalSuperBox/SparkBot-ng.git#egg=sparkbot

Run it!
-------

With that done, we're ready to go! Open a file called ``run.py`` and toss in some example code::

    from sparkbot import SparkBot
    from sparkbot.receivers.console import ConsoleReceiver

    bot = SparkBot()

    @bot.command("ping")
    def example(commandline):

        return "pong"

    if __name__ == "__main__":
        ConsoleReceiver(bot).cmdloop()

Great! Let's open it up::

    python run.py

    >Welcome to the SparkBot-ng console receiver. Type 'command' to execute a bot command. Type 'help' or '?' to list commands.
    >
    >(sparkbot)

Great! This is the SparkBot console receiver, a barebones way to test your bot without needing to connect to any cloud service. As the intro text suggests, let's try starting a command::

    (sparkbot) command ping
    >pong

That was easy! Let's break down what we just did.

The first part of the file is boring boilerplate to import and instance SparkBot::

    from sparkbot import SparkBot
    from sparkbot.receivers.console import ConsoleReceiver

    bot = SparkBot()

Now that we have the ``bot`` object, we can add a command to it using the ``SparkBot.command()`` decorator::

    @bot.command("ping")
    def example(commandline):

        return "pong"

This sets up a simple command which is called ``ping``. When users command the bot to run ``ping``, it executes the decorated function. The function name is ``example`` to show that the function name doesn't matter.

All command functions must take one argument, ``commandline`` is a good name for it. The argument is a list of strings, split with `shlex.split <https://docs.python.org/3.6/library/shlex.html#shlex.split>`_ internally. This gives you a nice list of tokens which the user sent in. To demonstrate, let's add another command before the ``if __name__ == "__main__":`` line::

    @bot.command("arguments")
    def arguments(commandline):

        for argument in commandline:
            yield argument

Let's run it. You'll need to ``exit`` your previous session and re-run the file, then::

    (sparkbot) command arguments a long "list of" things
    >arguments
    >a
    >long
    >list of
    >things

This shows our neatly tokenized list of arguments, including quoted strings!

Wait, ``yield``? Yes, we can use ``yield`` in our commands to return multiple strings to the user. This would be helpful if you had a very long-running command and wanted to give your user updates on the progress::

    import time

    @bot.command("forever")
    def takes_forever(commandline):

        yield("Okay, this will take a while!")
        time.sleep(10)
        yield("All done!")

Re-run the file, then:

.. code-block:: shell

    (sparkbot) command forever
    > Okay, this will take a while!
    # ... 10 second delay ...
    > All done!

Next steps
----------

With that, you've learned all you need to light your bot's fire using SparkBot. Writing commands is no harder than creating a function and returning strings!

Now that you're started on your journey, check out `Writing Commands`_ to learn more about writing more commands. If you're confident that you've got this down and want to get straight to deploying SparkBot for use on your favorite messaging service, check out the Deploy section to your left.
