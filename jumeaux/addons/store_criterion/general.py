# -*- coding:utf-8 -*-

"""For example of config
store_criterion:
  - name: jumeaux.addons.store_criterion.general
    config:
      statuses:
        - status
        - different
"""

import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from typing import Optional, List

from jumeaux.addons.store_criterion import StoreCriterionExecutor
from jumeaux.models import StoreCriterionAddOnPayload, Status

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, statuses: List[str] = None):
        self.statuses: TList[Status] = TList(statuses).map(lambda x: Status(x)) if statuses else TList()


class Executor(StoreCriterionExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: StoreCriterionAddOnPayload) -> StoreCriterionAddOnPayload:
        if payload.stored:
            return payload

        stored: bool = payload.status in self.config.statuses
        logger.debug(f"Store: {stored}")

        return StoreCriterionAddOnPayload.from_dict({
            "status": payload.status,
            "path": payload.path,
            "qs": payload.qs,
            "headers": payload.headers,
            "res_one": payload.res_one,
            "res_other": payload.res_other,
            "stored": stored
        })
