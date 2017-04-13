# -*- coding:utf-8 -*-

import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request, RequestAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, size):
        self.size: int = size


class Executor:
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: RequestAddOnPayload) -> RequestAddOnPayload:
        return RequestAddOnPayload.from_dict({
            'requests': payload.requests[0:self.config.size]
        })
