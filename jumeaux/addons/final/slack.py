# -*- coding:utf-8 -*-

"""
[Required environmental varialbles]
* SLACK_INCOMING_WEBHOOKS_URL
"""

import os
import sys

import requests
from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.final import FinalExecutor
from jumeaux.addons.utils import jinja2_format, get_jinja2_format_error
from jumeaux.logger import Logger
from jumeaux.models import Report, FinalAddOnPayload

logger: Logger = Logger(__name__)
LOG_PREFIX = "[final/slack]"
SLACK_AA = r"""
        ____  _            _
__/\__ / ___|| | __ _  ___| | __ __/\__
\    / \___ \| |/ _` |/ __| |/ / \    /
/_  _\  ___) | | (_| | (__|   <  /_  _\\
  \/   |____/|_|\__,_|\___|_|\_\   \/
"""


class Payload(OwlMixin):
    message_format: str
    channel: str
    username: str = 'jumeaux'
    icon_emoji: TOption[str]
    icon_url: TOption[str]


class Condition(OwlMixin):
    payload: Payload


class Config(OwlMixin):
    conditions: TList[Condition]


class SlackPayload(OwlMixin):
    text: str
    channel: str
    username: str
    icon_emoji: TOption[str]
    icon_url: TOption[str]
    link_names: int = 1


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})
        if "SLACK_INCOMING_WEBHOOKS_URL" not in os.environ:
            sys.exit('Environment variable SLACK_INCOMING_WEBHOOKS_URL is not specified. You need to set it.')

        errors: TList[str] = self.config.conditions\
            .map(lambda x: get_jinja2_format_error(x.payload.message_format).get())\
            .filter(lambda x: x is not None)
        if errors:
            logger.error(f"{LOG_PREFIX} Illegal format in `conditions[*].payload.message_format`.")
            logger.error(f"{LOG_PREFIX} Please check your configuration yaml files.")
            logger.error(f"{LOG_PREFIX} --- Error messages ---")
            errors.map(lambda x: logger.error(f"{LOG_PREFIX}   * `{x}`"))
            logger.error(f"{LOG_PREFIX} ---------------------", exit=True)

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        report: Report = payload.report

        logger.info_lv1(SLACK_AA)

        for c in self.config.conditions:  # type: Condition
            p = SlackPayload.from_dict({
                "text": jinja2_format(c.payload.message_format, report.to_dict()),
                "channel": c.payload.channel,
                "username": c.payload.username,
                "icon_emoji": c.payload.icon_emoji.get(),
                "icon_url": c.payload.icon_url.get(),
                "link_names": 1
            })
            requests.post(os.environ["SLACK_INCOMING_WEBHOOKS_URL"], data=p.to_json().encode('utf8'))
            logger.info_lv1(f"Send to {p.channel}")

        return payload
