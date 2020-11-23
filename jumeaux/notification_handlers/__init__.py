# -*- coding: utf-8 -*-

import sys

from jumeaux.logger import Logger
from jumeaux.models import Notifier
from jumeaux.domain.config.vo import NotifierType
from jumeaux.notification_handlers.base import NotificationHandler
from jumeaux.notification_handlers.slack import SlackNotificationHandler
from jumeaux.notification_handlers.slack2 import Slack2NotificationHandler

logger: Logger = Logger(__name__)


def create_notification_handler(notifier: Notifier) -> NotificationHandler:
    if notifier.type is NotifierType.SLACK:
        if notifier.version == 1:
            return SlackNotificationHandler(
                channel=notifier.channel.get(),
                username=notifier.username,
                icon_emoji=notifier.icon_emoji,
                icon_url=notifier.icon_url,
            )
        if notifier.version == 2:
            return Slack2NotificationHandler(use_blocks=notifier.use_blocks,)
    logger.error(f"Type {notifier.type.value}@v{notifier.version} is not valid.")
    sys.exit(1)
