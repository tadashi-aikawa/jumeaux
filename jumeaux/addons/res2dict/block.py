# -*- coding:utf-8 -*-

import re

from owlmixin import OwlMixin, TList

from jumeaux.addons.res2dict import Res2DictExecutor
from jumeaux.models import Res2DictAddOnPayload
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2dict/block]"


class Config(OwlMixin):
    force: bool = False
    header_regexp: str
    record_regexp: str
    mime_types: TList[str] = [
        'text/plain'
    ]


def config_generator(blockstr: str, header_regexp: str, record_regexp: str):
    key = None
    d: dict = {}

    # XXX: [""] means for the case which last line break is nothing
    for l in blockstr.splitlines() + [""]:
        if not l:
            if d:
                yield key, d
                d = {}
            continue

        r = re.findall(header_regexp, l)
        if r and len(r) == 1:
            key = r[0]
            continue

        b = re.findall(record_regexp, l)
        if b and len(b) == 1:
            d[b[0][0]] = b[0][1] if len(b[0]) > 1 else None


def to_dict(blockstr: str, header_regexp: str, record_regexp: str):
    return {k: v for k, v in config_generator(blockstr, header_regexp, record_regexp)}


class Executor(Res2DictExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        if not payload.result.is_none() and not self.config.force:
            logger.debug(f"{LOG_PREFIX} Skipped because result is nothing.")
            return payload

        mime_type: str = payload.response.mime_type.get()

        result: dict
        if self.config.force:
            logger.debug(f"{LOG_PREFIX} Force to convert to dict as block")
            result = to_dict(payload.response.text, self.config.header_regexp, self.config.record_regexp)
        elif mime_type in self.config.mime_types:
            logger.debug(f"{LOG_PREFIX} Convert to dict as block becuase mime-type is one of {self.config.mime_types}.")
            result = to_dict(payload.response.text, self.config.header_regexp, self.config.record_regexp)
        else:
            logger.debug(f"{LOG_PREFIX} Skipped because mime-type is not one of {self.config.mime_types}")
            result = None

        return Res2DictAddOnPayload.from_dict({
            "response": payload.response,
            "result": result
        })
