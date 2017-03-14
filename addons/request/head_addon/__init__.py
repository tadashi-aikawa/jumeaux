# -*- coding:utf-8 -*-

import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, size):
        self.size: int = size


def exec(requests: TList[Request], config_dict: dict) -> TList[Request]:
    config: Config = Config.from_dict(config_dict or {})
    return requests[0:config.size]
