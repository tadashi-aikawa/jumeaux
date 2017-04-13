# -*- coding:utf-8 -*-
from modules.models import Log2ReqsAddOnPayload


class Log2ReqsExecutor:
    def exec(self, payload: Log2ReqsAddOnPayload):
        raise NotImplementedError()
