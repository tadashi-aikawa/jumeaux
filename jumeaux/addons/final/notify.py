# -*- coding:utf-8 -*-

import sys

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.final import FinalExecutor
from jumeaux.addons.utils import jinja2_format, get_jinja2_format_error, when_optional_filter
from jumeaux.logger import Logger
from jumeaux.models import FinalAddOnPayload, Notifier, FinalAddOnReference, Report
from jumeaux.notification_handlers import create_notification_handler

logger: Logger = Logger(__name__)
LOG_PREFIX = "[final/notify]"


class Notify(OwlMixin):
    notifier: str
    message: str
    when: TOption[str]


class Config(OwlMixin):
    notifies: TList[Notify] = []


def send(message: str, notifier: Notifier) -> TOption[str]:
    logger.info_lv1(notifier.logging_message)
    return create_notification_handler(notifier).notify(message)


def need_to_notify(notify: Notify, report: Report) -> bool:
    if when_optional_filter(notify.when, report.to_dict(ignore_none=False)):
        logger.info_lv3(
            f"{LOG_PREFIX} Notify by {notify.notifier}. (notify.when => {notify.when.get_or('None')})"
        )
        return True
    else:
        logger.info_lv3(
            f"{LOG_PREFIX} Don't Notify by {notify.notifier}. (notify.when => {notify.when.get_or('None')}"
        )
        return False


class Executor(FinalExecutor):
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

    def exec(self, payload: FinalAddOnPayload, reference: FinalAddOnReference) -> FinalAddOnPayload:
        if reference.notifiers.is_none():
            logger.error(f"{LOG_PREFIX} There are no notifiers. Please set notifiers in config.")
            logger.error(
                f"{LOG_PREFIX} See https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/configuration/"
            )
            sys.exit(1)

        errors: TList[TOption[str]] = self.config.notifies.filter(
            lambda n: need_to_notify(n, payload.report)
        ).map(
            lambda x: send(
                jinja2_format(x.message, payload.report.to_dict(ignore_none=False)),
                reference.notifiers.get()
                .get(x.notifier)
                .get(),  # TODO: The case that notifier not found
            )
        )
        if errors.reject(lambda m: m.is_none()):
            errors.map(lambda m: m.map(logger.error))
            sys.exit(1)

        return payload
