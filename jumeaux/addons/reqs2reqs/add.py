# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TList, OwlObjectEnum

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload, Request


class Location(OwlObjectEnum):
    HEAD = ("head", lambda origin, reqs: reqs + origin)
    TAIL = ("tail", lambda origin, reqs: origin + reqs)

    @property
    def join(self):
        return self.object


class Config(OwlMixin):
    location: Location = 'head'
    reqs: TList[Request]


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': self.config.location.join(payload.requests, self.config.reqs)
        })
