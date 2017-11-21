# -*- coding:utf-8 -*-

import json

from owlmixin import OwlMixin, TList

from jumeaux.addons.res2dict import Res2DictExecutor
from jumeaux.models import Res2DictAddOnPayload


class Config(OwlMixin):
    force: bool = False
    mime_types: TList[str] = [
        'test/json', 'application/json'
    ]


class Executor(Res2DictExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        if not payload.result.is_none() and not self.config.force:
            return payload

        mime_type: str = payload.response.mime_type.get()
        return Res2DictAddOnPayload.from_dict({
            "response": payload.response,
            "result": json.loads(payload.response.text) \
                if self.config.force or mime_type in self.config.mime_types \
                else None
        })
