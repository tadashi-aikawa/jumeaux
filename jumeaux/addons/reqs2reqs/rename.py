# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.addons.utils import when_filter, when_optional_filter
from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Request, Reqs2ReqsAddOnPayload


class Condition(OwlMixin):
    name: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


def apply_first_condition(request: Request, conditions: TList[Condition]) -> Request:
    # TODO: remove TOption (owlmixin... find)
    condition: TOption[Condition] = TOption(
        conditions.find(lambda c: when_optional_filter(c.when, request.to_dict()))
    )
    if condition.is_none():
        return request

    name: TOption[str] = request.str_format(condition.get().name) \
        if when_optional_filter(condition.get().when, request.to_dict()) \
        else request.name

    return Request.from_dict({
        'name': name,
        'path': request.path,
        'qs': request.qs,
        'headers': request.headers,
    })


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.map(lambda r: apply_first_condition(r, self.config.conditions))
        })
