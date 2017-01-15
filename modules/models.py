# -*- coding: utf-8 -*-

from typing import Text, List

from owlmixin import OwlMixin, TDict, TList


class Request(OwlMixin):
    def __init__(self, path, qs=None, headers=None):
        self.path = path  # type: Text
        self.qs = TDict(qs) if qs else {}  # type: TDict[List[Text]]
        self.headers = TDict(headers) if headers else {}  # type: TDict[Text]
