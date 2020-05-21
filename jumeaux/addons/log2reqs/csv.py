# -*- coding:utf-8 -*-

import csv
import urllib.parse as urlparser
from typing import Iterable

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.log2reqs import Log2ReqsExecutor
from jumeaux.models import Request, Log2ReqsAddOnPayload


class Config(OwlMixin):
    encoding: str = "utf8"
    keep_blank: bool = False
    dialect: str = "excel"


class Executor(Log2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        """Transform csv as below.
            "title1", "GET", "/path1","a=1&b=2","header1=1&header2=2"
            "title2", "GET", "/path2","c=1"
            "title3", "GET", "/path3",,"header1=1&header2=2"
            "title4", "GET", "/path4"

        Exception:
            ValueError: If fomat is invalid.
        """
        outputs = []

        with open(payload.file, encoding=self.config.encoding) as f:
            rs: Iterable[dict] = csv.DictReader(
                f, ("name", "method", "path", "qs", "headers"), dialect=self.config.dialect
            )
            for r in rs:
                if len(r) > 5:
                    raise ValueError
                r["qs"] = urlparser.parse_qs(r["qs"], keep_blank_values=self.config.keep_blank)

                # XXX: This is bad implementation but looks simple...
                r["headers"] = urlparser.parse_qs(
                    r["headers"], keep_blank_values=self.config.keep_blank
                )
                for k, v in r["headers"].items():
                    r["headers"][k] = v[0]

                outputs.append(r)

        return Request.from_dicts(outputs)
