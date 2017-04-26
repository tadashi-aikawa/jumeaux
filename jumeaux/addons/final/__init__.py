# -*- coding:utf-8 -*-
from jumeaux.models import FinalAddOnPayload


class FinalExecutor:
    def exec(self, payload: FinalAddOnPayload):
        raise NotImplementedError()
