# -*- coding:utf-8 -*-

import xmltodict
from typing import Optional
from owlmixin import OwlMixin
from modules.models import Res2DictAddOnPayload


class Config(OwlMixin):
    def __init__(self, force: bool = False, force_encoding=None):
        self.force: bool = force
        self.force_encoding: Optional[str] = force_encoding


class Executor:
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload):
        if payload.result and not self.config.force:
            return payload

        mime_type = payload.response.headers.get('content-type').split(';')[0]
        encoding = self.config.force_encoding or payload.response.encoding

        return Res2DictAddOnPayload.from_dict({
            "response": payload.response,
            "result": xmltodict.parse(payload.response.text, encoding=encoding) \
                if self.config.force or mime_type in ('text/xml', 'application/xml') \
                else None
        })
