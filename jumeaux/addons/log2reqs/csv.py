# -*- coding:utf-8 -*-

import csv
import logging
import urllib.parse as urlparser

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.log2reqs import Log2ReqsExecutor
from jumeaux.models import Request, Log2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding='utf8', dialect='excel'):
        self.encoding: str = encoding
        self.dialect: str = dialect


class Executor(Log2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        """Transform csv as below.
            "title1","/path1","a=1&b=2","header1=1&header2=2"
            "title2","/path2","c=1"
            "title3","/path3",,"header1=1&header2=2"
            "title4","/path4"
    
        Exception:
            ValueError: If fomat is invalid.
        """
        outputs = []

        with open(payload.file, encoding=self.config.encoding) as f:
            rs = csv.DictReader(f, ('name', 'path', 'qs', 'headers'), restval={}, dialect=self.config.dialect)
            for r in rs:
                if len(r) > 4:
                    raise ValueError
                r['qs'] = urlparser.parse_qs(r['qs'])

                # XXX: This is bad implementation but looks simple...
                r['headers'] = urlparser.parse_qs(r['headers'])
                for k, v in r['headers'].items():
                    r['headers'][k] = v[0]

                outputs.append(r)

        return Request.from_dicts(outputs)
