# -*- coding:utf-8 -*-
from modules.models import FinalAddOnPayload


class FinalExecutor:
    def exec(self, payload: FinalAddOnPayload):
        raise NotImplementedError()
