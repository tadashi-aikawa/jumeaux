#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import requests

from jumeaux.logger import Logger
from jumeaux.models import *
from jumeaux.notification_handlers import NotificationHandler

logger: Logger = Logger(__name__)
LOG_PREFIX = "[notification_handlers]"


# See, https://app.slack.com/block-kit-builder
Block = any  # type: ignore


class SlackPayload(OwlMixin):
    text: TOption[str]
    thread_ts: TOption[str]
    blocks: TOption[TList[Block]]
    link_names: int = 1


class Slack2NotificationHandler(NotificationHandler):
    use_blocks: bool

    def __init__(self, use_blocks: bool):
        self.use_blocks = use_blocks

    def notify(self, message: str) -> TOption[str]:
        if "SLACK_INCOMING_WEBHOOKS_URL" not in os.environ:
            logger.warning(
                f"{LOG_PREFIX} SLACK_INCOMING_WEBHOOKS_URL is not defined in environmental variables."
            )
            logger.warning(f"{LOG_PREFIX} Please set SLACK_INCOMING_WEBHOOKS_URL.")
            logger.warning(f"{LOG_PREFIX} Skip notify to...")
            return TOption(None)

        text = None if self.use_blocks else message
        blocks = json.loads(message) if self.use_blocks else None

        p = SlackPayload.from_dict(
            {
                "text": text,
                "blocks": blocks,
                "thread_ts": os.environ.get("SLACK_THREAD_TS"),
                "link_names": 1,
            }
        )
        r: Response = Response.from_requests(
            requests.post(
                os.environ["SLACK_INCOMING_WEBHOOKS_URL"], data=p.to_json().encode("utf8")
            )
        )
        return TOption(r.text if not r.ok else None)
