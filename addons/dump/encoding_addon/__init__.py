# -*- coding:utf-8 -*-

from owlmixin import OwlMixin
from modules.models import DumpAddOnPayload
import logging

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding: str):
        self.encoding: str = encoding


class Executor:
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload):
        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": payload.body.decode(payload.encoding).encode(self.config.encoding),
            "encoding": self.config.encoding
        })
