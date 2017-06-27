# -*- coding:utf-8 -*-
from owlmixin import TList

from jumeaux.models import Log2ReqsAddOnPayload, Request


class Log2ReqsExecutor:
    def exec(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        raise NotImplementedError()
