# -*- coding:utf-8 -*-
from modules.models import JudgementAddOnPayload


class JudgementExecutor:
    def exec(self, payload: JudgementAddOnPayload):
        raise NotImplementedError()
