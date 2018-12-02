# -*- coding:utf-8 -*-

import random

import time
from owlmixin import OwlMixin

from jumeaux.addons.did_challenge import DidChallengeExecutor
from jumeaux.models import DidChallengeAddOnPayload, DidChallengeAddOnReference
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    max: float
    min: float


class Executor(DidChallengeExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DidChallengeAddOnPayload, referenece: DidChallengeAddOnReference) -> DidChallengeAddOnPayload:
        sec: float = random.uniform(self.config.min, self.config.max)

        logger.info_lv3(f"Sleep:  {sec:.2f} sec")
        time.sleep(sec)

        return payload
