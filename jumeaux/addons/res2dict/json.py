# -*- coding:utf-8 -*-

import json

from owlmixin import OwlMixin, TList

from jumeaux.addons.res2dict import Res2DictExecutor
from jumeaux.models import Res2DictAddOnPayload, DictOrList
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2dict/json]"


class Config(OwlMixin):
    force: bool = False


class Executor(Res2DictExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        if not payload.result.is_none() and not self.config.force:
            logger.debug(f"{LOG_PREFIX} Skipped because result is already existed.")
            return payload

        result: DictOrList  # type: ignore
        if self.config.force:
            logger.debug(f"{LOG_PREFIX} Force to convert to dict as json")
            result = json.loads(payload.response.text)
        elif payload.response.type == "json":
            logger.debug(f"{LOG_PREFIX} Convert to dict as json because this response is json.")
            result = json.loads(payload.response.text)
        else:
            logger.debug(f"{LOG_PREFIX} Skipped because this response is not json.")
            result = None

        return Res2DictAddOnPayload.from_dict({"response": payload.response, "result": result})
