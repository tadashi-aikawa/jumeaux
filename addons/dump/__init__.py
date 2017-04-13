# -*- coding:utf-8 -*-
from modules.models import DumpAddOnPayload


class DumpExecutor:
    def exec(self, payload: DumpAddOnPayload):
        raise NotImplementedError()
