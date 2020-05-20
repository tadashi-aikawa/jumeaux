# -*- coding:utf-8 -*-

import random

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.domain.config.vo import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        pass

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        random.shuffle(payload.requests)
        return payload
