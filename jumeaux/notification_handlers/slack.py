#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import requests

from jumeaux.models import *
from jumeaux.notification_handlers import NotificationHandler


class SlackPayload(OwlMixin):
    text: str
    channel: str
    username: str
    icon_emoji: TOption[str]
    icon_url: TOption[str]
    link_names: int = 1


class SlackNotificationHandler(NotificationHandler):
    channel: str
    username: str = 'jumeaux'
    icon_emoji: TOption[str]
    icon_url: TOption[str]

    def __init__(self, channel: str, username: str, icon_emoji: TOption[str], icon_url: TOption[str]):
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.icon_url = icon_url

    def notify(self, message: str) -> TOption[str]:
        p = SlackPayload.from_dict({
            "text": message,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji.map(lambda x: f':{x}:').get(),
            "icon_url": self.icon_url.get(),
            "link_names": 1
        })
        r: Response = Response.from_requests(
            requests.post(os.environ["SLACK_INCOMING_WEBHOOKS_URL"], data=p.to_json().encode('utf8'))
        )
        return TOption(r.text if not r.ok else None)
