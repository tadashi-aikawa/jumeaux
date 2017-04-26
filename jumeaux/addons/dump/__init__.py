# -*- coding:utf-8 -*-
from jumeaux.models import DumpAddOnPayload


class DumpExecutor:
    def exec(self, payload: DumpAddOnPayload):
        raise NotImplementedError()
