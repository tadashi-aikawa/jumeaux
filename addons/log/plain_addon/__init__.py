# -*- coding:utf-8 -*-

import urllib.parse as urlparser
import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding='utf8'):
        self.encoding: str = encoding


def main(file: str, config_dict: dict) -> TList[Request]:
    config: Config = Config.from_dict(config_dict or {})

    def line_to_request(line: str) -> Request:
        path = line.split('?')[0]
        qs = urlparser.parse_qs(line.split('?')[1]) if len(line.split('?')) > 1 else {}
        return Request.from_dict({"path": path, "qs": qs, "headers": {}})

    with open(file, encoding=config.encoding) as f:
        requests: TList[Request] = TList([x.rstrip() for x in f if x != '\n']).map(line_to_request)

    return requests
