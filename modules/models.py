# -*- coding: utf-8 -*-

from typing import List

from owlmixin import OwlMixin, TDict, TList


class Request(OwlMixin):
    def __init__(self, path, qs=None, headers=None):
        self.path = path  # type: str
        self.qs = TDict(qs) if qs else {}  # type: TDict[List[str]]
        self.headers = TDict(headers) if headers else {}  # type: TDict[str]
