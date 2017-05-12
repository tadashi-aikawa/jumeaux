# -*- coding:utf-8 -*-

import json

from owlmixin import OwlMixin
from typing import Optional

from jumeaux.addons.res2dict import Res2DictExecutor
from jumeaux.models import Res2DictAddOnPayload


class Config(OwlMixin):
    def __init__(self, force: bool = False, force_encoding=None):
        self.force: bool = force
        self.force_encoding: Optional[str] = force_encoding


class Executor(Res2DictExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload):
        if payload.result and not self.config.force:
            return payload

        content_type = payload.response.headers.get('content-type')
        mime_type = content_type.split(';')[0] if content_type else None
        encoding = self.config.force_encoding or payload.response.encoding

        return Res2DictAddOnPayload.from_dict({
            "response": payload.response,
            "result": json.loads(payload.response.text, encoding=encoding) \
                if self.config.force or mime_type in ('text/json', 'application/json') \
                else None
        })
