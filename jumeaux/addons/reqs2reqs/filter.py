# -*- coding:utf-8 -*-

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.conditions import RequestCondition, AndOr
from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Request, Reqs2ReqsAddOnPayload


class Config(OwlMixin):
    filters: TList[RequestCondition]
    and_or: AndOr = "and"
    negative: bool = False

    def fulfill(self, req: Request) -> bool:
        return self.negative ^ (self.and_or.check(self.filters.map(lambda x: x.fulfill(req))))


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.filter(lambda r: self.config.fulfill(r))
        })
