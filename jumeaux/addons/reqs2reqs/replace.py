# -*- coding:utf-8 -*-

import copy
import re
from datetime import datetime, timedelta

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict

from jumeaux.addons.conditions import RequestCondition, AndOr
from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Config as JumeauxConfig
from jumeaux.models import Request, Reqs2ReqsAddOnPayload


class Replacer(OwlMixin):
    conditions: TList[RequestCondition]
    and_or: AndOr = "and"
    negative: bool = False
    queries: TDict[TList[str]] = {}
    headers: TDict[str] = {}

    def fulfill(self, req: Request) -> bool:
        return self.negative ^ (self.and_or.check(self.conditions.map(lambda x: x.fulfill(req))))


class Config(OwlMixin):
    items: TList[Replacer]


def special_parse(value: str):
    m = re.search(r'^\$DATETIME\((.+)\)\((.+)\)$', value)
    return (datetime.now() + timedelta(seconds=int(m[2]))).strftime(m[1]) \
        if m else value


def replace_queries(req: Request, queries: TDict[TList[str]]) -> Request:
    copied = copy.deepcopy(req.qs)
    copied.update(queries.map_values(lambda vs: vs.map(special_parse)))
    req.qs = copied
    return req


def replace_headers(req: Request, headers: TDict[str]) -> Request:
    copied = copy.deepcopy(req.headers)
    copied.update(headers)
    req.headers = copied
    return req


def replace(req: Request, replacer: Replacer) -> Request:
    return replace_headers(replace_queries(req, replacer.queries), replacer.headers)


def apply_replacers(req: Request, replacers: TList[Replacer]) -> Request:
    return replacers.reduce(lambda req, rep: replace(req, rep) if rep.fulfill(req) else req, req)


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.map(lambda req: apply_replacers(req, self.config.items))
        })
