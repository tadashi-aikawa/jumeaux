# -*- coding:utf-8 -*-
from jumeaux.models import StoreCriterionAddOnPayload


class StoreCriterionExecutor:
    def exec(self, payload: StoreCriterionAddOnPayload) -> StoreCriterionAddOnPayload:
        raise NotImplementedError()
