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

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from owlmixin.owlenum import OwlObjectEnum
from typing import Optional

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
    def __init__(self, value: str, kind: str = "partial", negative: bool = False):
        self.value: str = value
        self.kind: Kind = Kind.from_symbol(kind)
        self.negative: bool = negative


class Condition(OwlMixin):
    def __init__(self, matchers: list, and_or: str = "or"):
        self.matchers: TList[Matcher] = Matcher.from_dicts(matchers)
        self.and_or: AndOr = AndOr.from_symbol(and_or)


class Filter(OwlMixin):
    def __init__(self, and_or: str = "and", name=None, path=None):
        self.and_or: AndOr = AndOr.from_symbol(and_or)
        self.name: Optional[Condition] = Condition.from_optional_dict(name)
        self.path: Optional[Condition] = Condition.from_optional_dict(path)


class Config(OwlMixin):
    def __init__(self, filters: list, and_or: str = "or"):
        self.filters: TList[Filter] = Filter.from_dicts(filters)
        self.and_or: AndOr = AndOr.from_symbol(and_or)


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
                is_fulfilled_condition(r.name, f.name) if f.name else True,
                is_fulfilled_condition(r.path, f.path) if f.path else True
            ])

        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.filter(lambda r: self.config.and_or.check(
                self.config.filters.map(lambda f: is_fulfilled_filter(r, f))))
        })
