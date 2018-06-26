# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.store_criterion import StoreCriterionExecutor, StoreCriterionAddOnReference
from jumeaux.addons.utils import when_filter
from jumeaux.logger import Logger
from jumeaux.models import StoreCriterionAddOnPayload, Status

logger: Logger = Logger(__name__)
LOG_PREFIX = "[store_criterion/free]"


class Config(OwlMixin):
    when_any: TOption[TList[str]]


class Executor(StoreCriterionExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: StoreCriterionAddOnPayload, reference: StoreCriterionAddOnReference) -> StoreCriterionAddOnPayload:
        if payload.stored:
            return payload

        if self.config.when_any.is_none():
            return StoreCriterionAddOnPayload.from_dict({"stored": True})

        matched_filter: str = self.config.when_any.get().find(lambda x: when_filter(x, reference.to_dict(ignore_none=False)))
        if matched_filter:
            logger.info_lv3(f"{LOG_PREFIX} Stored for `{matched_filter}`.")

        return StoreCriterionAddOnPayload.from_dict({
            "stored": bool(matched_filter)
        })
