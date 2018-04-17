# -*- coding:utf-8 -*-


from owlmixin import OwlMixin, TOption, TList, OwlObjectEnum

from jumeaux.addons.utils import exact_match
from jumeaux.models import Request


class AndOr(OwlObjectEnum):
    AND = ("and", all)
    OR = ("or", any)

    @property
    def check(self):
        return self.object


class Matcher(OwlMixin):
    regexp: str
    negative: bool = False

    def fulfill(self, v: str) -> bool:
        return self.negative ^ exact_match(v, self.regexp)


class Matchers(OwlMixin):
    items: TList[Matcher]
    and_or: AndOr = "and"  # type: ignore # Prevent for enum problem
    negative: bool = False

    def fulfill(self, v: str) -> bool:
        return self.negative ^ (self.and_or.check(self.items.map(lambda x: x.fulfill(v))))


class RequestCondition(OwlMixin):
    name: TOption[Matchers]
    path: TOption[Matchers]
    and_or: AndOr = "and"  # type: ignore # Prevent for enum problem
    negative: bool = False

    def fulfill(self, r: Request) -> bool:
        return self.negative ^ (self.and_or.check([
            self.name.get().fulfill(r.name.get()) if self.name.get() else True,
            self.path.get().fulfill(r.path) if self.path.get() else True,
        ]))
