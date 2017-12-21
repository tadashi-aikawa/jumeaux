# -*- coding:utf-8 -*-

from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload


class Reqs2ReqsExecutor:
    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        raise NotImplementedError()
