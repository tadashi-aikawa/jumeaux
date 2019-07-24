# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import FinalAddOnPayload, FinalAddOnReference
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    sysout: bool = False
    indent: TOption[int]


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload, reference: FinalAddOnReference) -> FinalAddOnPayload:
        if self.config.sysout:
            print(payload.report.to_json(indent=self.config.indent.get()))
        else:
            payload.report.to_jsonf(
                f"{payload.result_path}/report.json",
                encoding=payload.output_summary.encoding,
                indent=self.config.indent.get(),
            )
        return payload
