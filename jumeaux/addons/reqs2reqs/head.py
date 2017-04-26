# -*- coding:utf-8 -*-

import logging

from owlmixin import OwlMixin

from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Reqs2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, size):
        self.size: int = size


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests[0:self.config.size]
        })
