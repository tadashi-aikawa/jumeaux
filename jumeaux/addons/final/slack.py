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
from jumeaux.logger import Logger
from jumeaux.models import Report, FinalAddOnPayload

logger: Logger = Logger(__name__)


class SlackPayload(OwlMixin):
    text: str
    channel: str
    username: str
    icon_emoji: TOption[str]
    icon_url: TOption[str]
    link_names: int = 1


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


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})
        if not "SLACK_INCOMING_WEBHOOKS_URL" in os.environ:
            sys.exit('Environment variable SLACK_INCOMING_WEBHOOKS_URL is not specified. You need to set it.')

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        report: Report = payload.report

        logger.info_lv1("""
        ____  _            _           
__/\__ / ___|| | __ _  ___| | __ __/\__
\    / \___ \| |/ _` |/ __| |/ / \    /
/_  _\  ___) | | (_| | (__|   <  /_  _\\
  \/   |____/|_|\__,_|\___|_|\_\   \/  
""")

        for c in self.config.conditions:  # type: Condition
            p = SlackPayload.from_dict({
                "text": c.payload.message_format.format(**report.to_dict()),
                "channel": c.payload.channel,
                "username": c.payload.username,
                "icon_emoji": c.payload.icon_emoji.get(),
                "icon_url": c.payload.icon_url.get(),
                "link_names": 1
            })
            requests.post(os.environ["SLACK_INCOMING_WEBHOOKS_URL"], data=p.to_json().encode('utf8'))
            logger.info_lv1(f"Send to {p.channel}")

        return payload
