# -*- coding:utf-8 -*-

import re

from owlmixin import OwlMixin, TList

from jumeaux.addons.res2dict import Res2DictExecutor
from jumeaux.models import Res2DictAddOnPayload


class Config(OwlMixin):
    force: bool = False
    mime_types: TList[str] = [
        'text/plain'
    ]


def config_generator(plain):
    key = None
    d = {}

    # XXX: [""] means for the case which last line break is nothing
    for l in plain.splitlines() + [""]:
        if not l:
            if d:
                yield key, d
                d = {}
            continue

        r = re.findall('^\d+\)(.+)', l)
        if r and r[0]:
            key = r[0]
            continue

        k, v = l.split(' ', 1)
        d[k] = v


def to_dict(plain: str):
    return {k: v for k, v in config_generator(plain)}


class Executor(Res2DictExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        if not payload.result.is_none() and not self.config.force:
            return payload

        mime_type: str = payload.response.mime_type.get()
        return Res2DictAddOnPayload.from_dict({
            "response": payload.response,
            "result": to_dict(payload.response.text) \
                if self.config.force or mime_type in self.config.mime_types \
                else None
        })
