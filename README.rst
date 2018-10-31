########
SparkBot
########

How do I get support?
=====================

If you experience issues with SparkBot, please visit the issue tracker.

How can I contribute?
=====================

Thanks for asking! Here's how you can test the SparkBot code or build its documentation locally:

Test the code
-------------

To develop on SparkBot, you can do the following::

    pip install -e .[dev]

When you're ready to commit, run the bot's tests first. You will need a copy of `nodejs`_ installed,
then run the following::

    pytest

Build the documentation
-----------------------

To build the documentation, cd into the ``doc`` folder and run the following::

    pip install -e ../[dev]
    make html

If you are on Windows, use ``make.bat`` rather than ``make``.

The documentation will be located in the ``doc/_build/`` directory.

License
-------

SparkBot is copyright Dalton Durst, 2018. It is licensed under the Apache license, version 2.0. See
the LICENSE file for more details.

.. _the documentation: http://sparkbot.readthedocs.io/en/latest/
.. _sparkbot 1.0.0: https://github.com/UniversalSuperBox/SparkBot/milestone/1
.. _nodejs: https://nodejs.org/en/download/
