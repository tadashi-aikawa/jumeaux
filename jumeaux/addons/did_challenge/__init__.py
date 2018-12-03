# -*- coding:utf-8 -*-
from jumeaux.models import DidChallengeAddOnPayload, DidChallengeAddOnReference


class DidChallengeExecutor:
    def exec(self, payload: DidChallengeAddOnPayload, referenece: DidChallengeAddOnReference) -> DidChallengeAddOnPayload:
        raise NotImplementedError()
