# -*- coding:utf-8 -*-

from owlmixin import OwlMixin
from modules.models import ResponseAddOnPayload
import logging

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding):
        self.encoding: str = encoding


def exec(payload: ResponseAddOnPayload, config_dict: dict):
    config: Config = Config.from_dict(config_dict or {})

    return ResponseAddOnPayload.from_dict({
        "response": payload.response,
        "body": payload.body.decode(payload.encoding).encode(config.encoding),
        "encoding": config.encoding
    })
