# -*- coding:utf-8 -*-
from jumeaux.models import FinalAddOnPayload, FinalAddOnReference


class FinalExecutor:
    def exec(self, payload: FinalAddOnPayload, reference: FinalAddOnReference) -> FinalAddOnPayload:
        raise NotImplementedError()
