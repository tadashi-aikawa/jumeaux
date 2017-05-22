# -*- coding:utf-8 -*-
from jumeaux.models import JudgementAddOnPayload


class JudgementExecutor:
    def exec(self, payload: JudgementAddOnPayload) -> JudgementAddOnPayload:
        raise NotImplementedError()
