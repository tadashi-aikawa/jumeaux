# -*- coding:utf-8 -*-

import logging

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
        """Transform from json to Request
    
        Exception:
            ValueError: If path does not exist.
        """
        try:
            return Request.from_jsonf_to_list(payload.file, encoding=self.config.encoding)
        except TypeError as e:
            raise ValueError(e)
