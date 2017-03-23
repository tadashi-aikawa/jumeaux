# -*- coding:utf-8 -*-

import logging
import re
from typing import Optional

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from owlmixin.owlenum import OwlEnum
from modules.models import Request

logger = logging.getLogger(__name__)


class Kind(OwlEnum):
    PERFECT = "perfect"
    PARTIAL = "partial"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    REGEXP = "regexp"


class AndOr(OwlEnum):
    AND = "and"
    OR = "or"


class Matcher(OwlMixin):
    def __init__(self, value: str, kind: str = "partial", negative: bool = False):
        self.value: str = value
        self.kind: Kind = Kind(kind)
        self.negative: bool = negative


class Condition(OwlMixin):
    def __init__(self, matchers: list, and_or: str = "or"):
        self.matchers: TList[Matcher] = Matcher.from_dicts(matchers)
        self.and_or: AndOr = AndOr(and_or)


class Filter(OwlMixin):
    def __init__(self, name=None, path=None):
        self.name: Optional[Condition] = Condition.from_optional_dict(name)
        self.path: Optional[Condition] = Condition.from_optional_dict(path)


class Config(OwlMixin):
    def __init__(self, filters_or: list):
        self.filters_or: TList[Filter] = Filter.from_dicts(filters_or)


def exec(requests: TList[Request], config_dict: dict) -> TList[Request]:
    config: Config = Config.from_dict(config_dict or {})

    def is_fulfilled_matcher(value: str, m: Matcher) -> bool:
        is_fulfilled = funcs_by_kind = {
            Kind.PERFECT: lambda v: v == m.value,
            Kind.PARTIAL: lambda v: m.value in v,
            Kind.PREFIX: lambda v: v.startswith(m.value),
            Kind.SUFFIX: lambda v: v.endswith(m.value),
            Kind.REGEXP: lambda v: re.search(m.value, v)
        }[m.kind](value)
        return m.negative ^ bool(is_fulfilled)

    def is_fulfilled_condition(value: str, c: Condition) -> bool:
        func = all if c.and_or is AndOr.AND else any
        return func(c.matchers.filter(lambda m: is_fulfilled_matcher(value, m)))

    def is_fulfilled_filter(r: Request, f: Filter) -> bool:
        return all([
            is_fulfilled_condition(r.name, f.name) if f.name else True,
            is_fulfilled_condition(r.path, f.path) if f.path else True
        ])

    return requests.filter(lambda r: config.filters_or.any(lambda f: is_fulfilled_filter(r, f)))
