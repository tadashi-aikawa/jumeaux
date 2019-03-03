# -*- coding:utf-8 -*-

import sys

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.final import FinalExecutor
from jumeaux.addons.utils import jinja2_format, get_jinja2_format_error
from jumeaux.logger import Logger
from jumeaux.models import FinalAddOnPayload, Notifier, FinalAddOnReference
from jumeaux.notification_handlers import create_notification_handler

logger: Logger = Logger(__name__)
LOG_PREFIX = "[final/notify]"


class Notify(OwlMixin):
    notifier: str
    message: str


class Config(OwlMixin):
    notifies: TList[Notify] = []


def send(message: str, notifier: Notifier) -> TOption[str]:
    logger.info_lv1(notifier.logging_message)
    return create_notification_handler(notifier).notify(message)


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

        errors: TList[str] = self.config.notifies \
            .map(lambda x: get_jinja2_format_error(x.message).get()) \
            .filter(lambda x: x is not None)
        if errors:
            logger.error(f"{LOG_PREFIX} Illegal format in `notifies[*].message`.")
            logger.error(f"{LOG_PREFIX} Please check your configuration yaml files.")
            logger.error(f"{LOG_PREFIX} --- Error messages ---")
            errors.map(lambda x: logger.error(f"{LOG_PREFIX}   * `{x}`"))
            logger.error(f"{LOG_PREFIX} ---------------------", exit=True)

    def exec(self, payload: FinalAddOnPayload, reference: FinalAddOnReference) -> FinalAddOnPayload:
        errors: TList[TOption[str]] = self.config.notifies.map(lambda x: send(
            jinja2_format(x.message, payload.report.to_dict(ignore_none=False)),
            reference.notifiers.get().get(x.notifier)
        ))
        if errors:
            errors.map(lambda m: m.map(logger.error))
            sys.exit(1)

        return payload

