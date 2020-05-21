# -*- coding:utf-8 -*-

import sys

from owlmixin import OwlMixin, TList, TOption

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.addons.utils import jinja2_format, get_jinja2_format_error
from jumeaux.logger import Logger
from jumeaux.domain.config.vo import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload, Notifier
from jumeaux.notification_handlers import create_notification_handler

logger: Logger = Logger(__name__)
LOG_PREFIX = "[reqs2reqs/empty_guard]"


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

        errors: TList[str] = self.config.notifies.map(
            lambda x: get_jinja2_format_error(x.message).get()
        ).filter(lambda x: x is not None)
        if errors:
            logger.error(f"{LOG_PREFIX} Illegal format in `notifies[*].message`.")
            logger.error(f"{LOG_PREFIX} Please check your configuration yaml files.")
            logger.error(f"{LOG_PREFIX} --- Error messages ---")
            errors.map(lambda x: logger.error(f"{LOG_PREFIX}   * `{x}`"))
            logger.error(f"{LOG_PREFIX} ---------------------", exit=True)

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        if not payload.requests:
            logger.warning("Requests are empty. Exit executor.")
            # TODO: Error handling
            errors: TList[TOption[str]] = self.config.notifies.map(
                lambda x: send(
                    jinja2_format(x.message, config.to_dict(ignore_none=False)),
                    config.notifiers.get()
                    .get(x.notifier)
                    .get(),  # TODO: The case that notifier not found
                )
            )
            errors.map(lambda m: m.map(logger.error))
            sys.exit(1)

        return Reqs2ReqsAddOnPayload.from_dict({"requests": payload.requests})
