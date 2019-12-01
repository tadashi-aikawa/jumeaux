# -*- coding:utf-8 -*-

import urllib.parse as urlparser
from typing import Dict, List

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.log2reqs import Log2ReqsExecutor
from jumeaux.logger import Logger
from jumeaux.models import Request, Log2ReqsAddOnPayload

logger: Logger = Logger(__name__)
LOG_PREFIX = "[log2reqs/plain]"


class Config(OwlMixin):
    encoding: str = "utf8"
    keep_blank: bool = False
    candidate_for_url_encodings: TList[str] = []


def guess_url_encoding(query_str: str, encodings: TList[str]) -> TOption[str]:
    for e in encodings:
        try:
            urlparser.parse_qs(query_str, encoding=e, errors="strict")
            return TOption(e)
        except UnicodeDecodeError:
            pass

    return TOption(None)


class Executor(Log2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        def line_to_request(line: str, seq: int) -> Request:
            logger.debug(f"{LOG_PREFIX} ---- {seq} ----")

            path = line.split("?")[0]
            logger.debug(f"{LOG_PREFIX} [path] {path}")

            url_encoding = "utf-8"
            qs: Dict[str, List[str]] = {}
            if len(line.split("?")) > 1:
                url_encoding = guess_url_encoding(
                    line.split("?")[1], self.config.candidate_for_url_encodings
                ).get_or("utf-8")
                qs = urlparser.parse_qs(
                    line.split("?")[1],
                    keep_blank_values=self.config.keep_blank,
                    encoding=url_encoding,
                )
            logger.debug(f"{LOG_PREFIX} [qs] ({url_encoding}) {qs}")

            return Request.from_dict(
                {"path": path, "qs": qs, "headers": {}, "url_encoding": url_encoding}
            )

        with open(payload.file, encoding=self.config.encoding) as f:
            requests: TList[Request] = TList([x.rstrip() for x in f if x != "\n"]).emap(
                lambda x, i: line_to_request(x, i)
            )

        return requests
