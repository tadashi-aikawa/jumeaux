# -*- coding:utf-8 -*-

"""
[Required environmental varialbles]
* SLACK_INCOMING_WEBHOOKS_URL
"""

import os
import logging
from typing import Optional

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Report, OutputSummary
import requests

logger = logging.getLogger(__name__)


class SlackPayload(OwlMixin):
    def __init__(self, text, channel, username, icon_emoji=None, icon_url=None, link_names=1):
        self.text: str = text
        self.channel: str = channel
        self.username: str = username
        self.icon_emoji: Optional[str] = icon_emoji
        self.icon_url: Optional[str] = icon_url
        self.link_names: int = link_names


class Payload(OwlMixin):
    def __init__(self, message_format, channel, username='gemini', icon_emoji=None, icon_url=None):
        self.message_format: str = message_format
        self.channel: str = channel
        self.username: str = username
        self.icon_emoji: Optional[str] = icon_emoji
        self.icon_url: Optional[str] = icon_url


class Condition(OwlMixin):
    def __init__(self, payload):
        # TODO: condition
        self.payload: Payload = Payload.from_dict(payload)


class Config(OwlMixin):
    def __init__(self, conditions):
        self.conditions: TList[Condition] = Condition.from_dicts(conditions)


def exec(report: Report, config_dict: dict, output_summary: OutputSummary):
    config: Config = Config.from_dict(config_dict or {})

    for c in config.conditions:  # type: Condition
        p = SlackPayload.from_dict({
            "text": c.payload.message_format.format(report.to_dict()),
            "channel": c.payload.channel,
            "username": c.payload.username,
            "icon_emoji": c.payload.icon_emoji,
            "icon_url": c.payload.icon_url,
            "link_names": 1
        })
        requests.post(os.environ["SLACK_INCOMING_WEBHOOKS_URL"], data=p.to_json().encode('utf8'))

    return report
