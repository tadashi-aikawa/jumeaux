# -*- coding:utf-8 -*-

import json

from owlmixin import OwlMixin, TList

from jumeaux.addons.dump import DumpExecutor
from jumeaux.models import DumpAddOnPayload


class Config(OwlMixin):
    default_encoding: str = 'utf8'
    force: bool = False


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        encoding: str = payload.encoding.get_or(self.config.default_encoding)

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": json.dumps(
                json.loads(payload.body.decode(encoding, errors='replace')),
                ensure_ascii=False, indent=4, sort_keys=True
            ).encode(encoding, errors='replace') \
                if self.config.force or payload.response.type == 'json' \
                else payload.body,
            "encoding": encoding
        })
