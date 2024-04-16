# -*- coding:utf-8 -*-


from owlmixin import OwlMixin

from jumeaux.addons.dump import DumpExecutor
from jumeaux.logger import Logger
from jumeaux.models import DumpAddOnPayload

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    encoding: str


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        return DumpAddOnPayload.from_dict(
            {
                "response": payload.response,
                "body": payload.body.decode(payload.encoding.get()).encode(
                    self.config.encoding
                ),
                "encoding": self.config.encoding,
            }
        )
