# -*- coding:utf-8 -*-

import logging
import random

from owlmixin import OwlMixin

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Reqs2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        pass

    def exec(self, payload: Reqs2ReqsAddOnPayload) -> Reqs2ReqsAddOnPayload:
        random.shuffle(payload.requests)
        return payload
