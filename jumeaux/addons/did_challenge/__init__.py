# -*- coding:utf-8 -*-
from jumeaux.models import DidChallengeAddOnPayload


class DidChallengeExecutor:
    def exec(self, payload: DidChallengeAddOnPayload) -> DidChallengeAddOnPayload:
        raise NotImplementedError()
