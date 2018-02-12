# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, OwlEnum, TList

from jumeaux.addons.final import FinalExecutor
from jumeaux.logger import Logger
from jumeaux.models import Report, FinalAddOnPayload, Trial

logger: Logger = Logger(__name__)


class Column(OwlEnum):
    SEQ = 'seq'
    NAME = 'name'
    PATH = 'path'
    STATUS = 'status'


class Config(OwlMixin):
    columns: TList[Column]


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        trials: TList[Trial] = payload.report.trials

        logger.info_lv1(trials.to_table(self.config.columns.map(lambda x: x.value)))
        return payload

