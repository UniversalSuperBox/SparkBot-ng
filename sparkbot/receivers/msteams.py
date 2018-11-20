"""Package for Microsoft Teams bot connector receiver"""

import json
from os import environ
import asyncio

import falcon

from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext)

def sync_run(coroutine):
    event_loop = None
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
    return event_loop.run_until_complete(coroutine)

def create(bot, name, app_id=None, app_password=None):
    """Returns a Falcon.API instance configured for receiving calls from Microsoft Teams

    :param bot: Bot instance for this receiver to control
    :type bot: :class:`sparkbot.SparkBot`

    :param name: The MS Teams name of the bot in Microsoft Teams, which will be
                 removed from incoming messages before dispatch

    :param app_id: The Microsoft App ID to authenticate as

    :app_password: The Microsoft App Password to authenticate with

    If ``app_id`` and ``app_password`` are not passed, ``MICROSOFT_APP_ID`` and
    ``MICROSOFT_APP_PASSWORD`` from the environment will be used, respectively.
    """

    app = falcon.API()
    app.add_route("/message", ReceiverResource(bot, name, app_id=app_id, app_password=app_password))

    return app

class ReceiverResource():
    """Falcon behavior for Microsoft Teams bot receiver. Use :func:`create` to set up.
    """

    def __init__(self, bot, name, app_id=None, app_password=None):
        """Create a receiver behavior object which acts on bot

        :param bot: Bot instance for this receiver to control
        :type bot: :class:`sparkbot.SparkBot`

        :param name: The MS Teams name of the bot in Microsoft Teams, which will be
                     removed from incoming messages before dispatch

        :param app_id: The Microsoft App ID to authenticate as

        :param app_password: The Microsoft App Password to authenticate with

        If ``app_id`` and ``app_password`` are not passed, ``MICROSOFT_APP_ID`` and
        ``MICROSOFT_APP_PASSWORD`` from the environment will be used, respectively.
        """

        if not app_id:
            try:
                app_id = environ["MICROSOFT_APP_ID"]
            except KeyError:
                raise KeyError("MICROSOFT_APP_ID not found in environment and not passed in msteams.create() call")

        if not app_password:
            try:
                app_password = environ["MICROSOFT_APP_PASSWORD"]
            except KeyError:
                raise KeyError("MICROSOFT_APP_PASSWORD not found in environment and not passed in msteams.create() call")

        settings = BotFrameworkAdapterSettings(app_id, app_password)
        self.adapter = BotFrameworkAdapter(settings)
        self.name = name
        self.bot = bot

    def on_post(self, req, resp):

        try:
            auth_header = req.headers['AUTHORIZATION']
        except KeyError:
            resp.status = falcon.HTTP_403
            return

        if req.content_length:
            activity = Activity().deserialize(json.load(req.stream))

        sync_run(self.adapter.authenticate_request(activity, auth_header))
        commandline = activity.text
        conversation = activity.conversation
        context = TurnContext(self.adapter, activity)

        commandline = commandline.replace("<at>{}</at>".format(self.name), "")

        sync_run(context.send_activity(self.bot.command_dispatcher(commandline)))
