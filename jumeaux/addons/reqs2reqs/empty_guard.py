# -*- coding:utf-8 -*-

import sys

from owlmixin import OwlMixin, TList, TOption

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload, Notifier
from jumeaux.notification_handlers import create_notification_handler
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class Notify(OwlMixin):
    notifier: str
    message: str


class Config(OwlMixin):
    notifies: TList[Notify] = []


def send(message: str, notifier: Notifier) -> TOption[str]:
    logger.info_lv1(notifier.logging_message)
    return create_notification_handler(notifier).notify(message)


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        if not payload.requests:
            logger.warning("Requests are empty. Exit executor.")
            # TODO: Error handling
            errors: TList[TOption[str]] = self.config.notifies.map(lambda x: send(
                x.message.format(**config.to_dict(ignore_none=False)),
                config.notifiers.get().get(x.notifier)
            ))
            errors.map(lambda m: m.map(logger.error))
            sys.exit(1)

        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests
        })
