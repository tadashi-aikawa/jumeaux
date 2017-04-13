# -*- coding:utf-8 -*-

import logging
import random

from owlmixin import OwlMixin

from modules.models import RequestAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self):
        pass


class Executor:
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: RequestAddOnPayload) -> RequestAddOnPayload:
        random.shuffle(payload.requests)
        return payload
