# -*- coding: utf-8 -*-

import sys

from jumeaux.logger import Logger
from jumeaux.models import Notifier, NotifierType
from jumeaux.notification_handlers.base import NotificationHandler
from jumeaux.notification_handlers.slack import SlackNotificationHandler

logger: Logger = Logger(__name__)


def create_notification_handler(notifier: Notifier) -> NotificationHandler:
    if notifier.type is NotifierType.SLACK:
        return SlackNotificationHandler(
            channel=notifier.channel,
            username=notifier.username,
            icon_emoji=notifier.icon_emoji,
            icon_url=notifier.icon_url
        )
    logger.error(f"Type {notifier.type} is not valid.")
    sys.exit(1)
