# -*- coding:utf-8 -*-

"""For example of config

reqs2reqs:
  - name: addons.reqs2reqs.filter
    config:
      filters:
        - path:
            matchers:
              - value: list
              - value: route
                kind: suffix
            and_or: or
        - name:
            matchers:
              - value: 一覧
                negative: true
      and_or: and
"""

import logging
import re

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList
from owlmixin.owlenum import OwlObjectEnum

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Request, Reqs2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Kind(OwlObjectEnum):
    PERFECT = ("perfect", lambda value, pattern: value == pattern)
    PARTIAL = ("partial", lambda value, pattern: pattern in value)
    PREFIX = ("prefix", lambda value, pattern: value.startswith(pattern))
    SUFFIX = ("suffix", lambda value, pattern: value.endswith(pattern))
    REGEXP = ("regexp", lambda value, pattern: re.search(pattern, value))

    @property
    def judge(self):
        return self.object


class AndOr(OwlObjectEnum):
    AND = ("and", all)
    OR = ("or", any)

    @property
    def check(self):
        return self.object


class Matcher(OwlMixin):
    value: str
    kind: Kind = 'partial'
    negative: bool = False


class Condition(OwlMixin):
    matchers: TList[Matcher]
    and_or: AndOr = 'or'


class Filter(OwlMixin):
    and_or: AndOr = 'and'
    name: TOption[Condition]
    path: TOption[Condition]


class Config(OwlMixin):
    filters: TList[Filter]
    and_or: AndOr


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload) -> Reqs2ReqsAddOnPayload:
        def is_fulfilled_matcher(value: str, m: Matcher) -> bool:
            return m.negative ^ bool(m.kind.judge(value, m.value))

        def is_fulfilled_condition(value: str, c: Condition) -> bool:
            return c.and_or.check(c.matchers.map(lambda m: is_fulfilled_matcher(value, m)))

        def is_fulfilled_filter(r: Request, f: Filter) -> bool:
            return f.and_or.check([
                is_fulfilled_condition(r.name, f.name.get()) if f.name.get() else True,
                is_fulfilled_condition(r.path, f.path.get()) if f.path.get() else True
            ])

        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.filter(lambda r: self.config.and_or.check(
                self.config.filters.map(lambda f: is_fulfilled_filter(r, f))))
        })
