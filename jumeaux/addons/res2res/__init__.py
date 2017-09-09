# -*- coding:utf-8 -*-
from jumeaux.models import Res2ResAddOnPayload


class Res2ResExecutor:
    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        raise NotImplementedError()
