# -*- coding:utf-8 -*-

import logging
import urllib.parse as urlparser

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.log2reqs import Log2ReqsExecutor
from jumeaux.models import Request, Log2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding='utf8'):
        self.encoding: str = encoding


class Executor(Log2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        def line_to_request(line: str) -> Request:
            path = line.split('?')[0]
            qs = urlparser.parse_qs(line.split('?')[1]) if len(line.split('?')) > 1 else {}
            return Request.from_dict({"path": path, "qs": qs, "headers": {}})

        with open(payload.file, encoding=self.config.encoding) as f:
            requests: TList[Request] = TList([x.rstrip() for x in f if x != '\n']).map(line_to_request)

        return requests
