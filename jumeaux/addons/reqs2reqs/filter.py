# -*- coding:utf-8 -*-

from owlmixin import OwlMixin

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.utils import when_filter
from jumeaux.domain.config.vo import Config as JumeauxConfig
from jumeaux.models import Reqs2ReqsAddOnPayload


class Config(OwlMixin):
    when: str


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict(
            {
                "requests": payload.requests.filter(
                    lambda r: when_filter(self.config.when, r.to_dict())
                )
            }
        )
