# -*- coding:utf-8 -*-
from jumeaux.models import JudgementAddOnPayload, JudgementAddOnReference


class JudgementExecutor:
    def exec(self, payload: JudgementAddOnPayload, reference: JudgementAddOnReference) -> JudgementAddOnPayload:
        raise NotImplementedError()
