# -*- coding:utf-8 -*-
from jumeaux.models import StoreCriterionAddOnPayload, StoreCriterionAddOnReference


class StoreCriterionExecutor:
    def exec(self, payload: StoreCriterionAddOnPayload, reference: StoreCriterionAddOnReference) -> StoreCriterionAddOnPayload:
        raise NotImplementedError()
