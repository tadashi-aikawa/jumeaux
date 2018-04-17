# -*- coding:utf-8 -*-

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.store_criterion import StoreCriterionExecutor, StoreCriterionAddOnReference
from jumeaux.logger import Logger
from jumeaux.models import StoreCriterionAddOnPayload, Status

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    statuses: TList[Status]


class Executor(StoreCriterionExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: StoreCriterionAddOnPayload, reference: StoreCriterionAddOnReference) -> StoreCriterionAddOnPayload:
        if payload.stored:
            return payload

        stored: bool = reference.status in self.config.statuses
        logger.debug(f"Store: {stored}")

        return StoreCriterionAddOnPayload.from_dict({
            "stored": stored
        })
