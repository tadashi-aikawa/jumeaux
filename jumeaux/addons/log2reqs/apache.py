# -*- coding:utf-8 -*-

import logging
import re
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
        """Transform apache access_log as below.
            000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
            000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path2?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"
    
        Exception:
            ValueError: If url is invalid.
        """
        outputs = []
        with open(payload.file, encoding=self.config.encoding) as f:
            for r in f:
                url = r.split(' ')[6]
                if len(url.split('?')) > 2:
                    raise ValueError

                path = url.split('?')[0]
                if len(url.split('?')) > 1:
                    qs = urlparser.parse_qs(url.split('?')[1])
                else:
                    qs = {}

                headers = {}
                for h in re.compile('"([^= ]+=[^ ]+)"').findall(r):
                    k, v = h.split('=')
                    if v != '-':
                        headers[k] = v
                outputs.append({"path": path, "qs": qs, "headers": headers})

        return Request.from_dicts(outputs)
