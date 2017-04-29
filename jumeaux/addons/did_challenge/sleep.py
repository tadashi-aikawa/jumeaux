# -*- coding:utf-8 -*-

"""For example of config
did_challenge:
- name: jumeaux.addons.did_challenge.sleep
  config:
    min: 0.1
    max: 1.0
"""

import logging
import random

import time
from owlmixin import OwlMixin

from jumeaux.addons.did_challenge import DidChallengeExecutor
from jumeaux.models import DidChallengeAddOnPayload


logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, max: float, min: float):
        self.max: float = max
        self.min: float = min


class Executor(DidChallengeExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DidChallengeAddOnPayload):
        sec: float = random.uniform(self.config.min, self.config.max)

        logger.info(f"Sleep:  {sec:.2f} sec")
        time.sleep(sec)

        return payload
