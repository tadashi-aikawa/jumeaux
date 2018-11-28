# -*- coding:utf-8 -*-

import random

import time
from owlmixin import OwlMixin, TOption, TList

from jumeaux.addons.did_challenge import DidChallengeExecutor
from jumeaux.addons.utils import when_optional_filter
from jumeaux.models import DidChallengeAddOnPayload, Trial
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)
LOG_PREFIX = "[did_challenge/tag]"


class Condition(OwlMixin):
    tag: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


class Executor(DidChallengeExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DidChallengeAddOnPayload) -> DidChallengeAddOnPayload:
        # TODO: remove TOption (owlmixin... find)
        conditions: TList[Condition] = self.config.conditions.filter(
            lambda c: when_optional_filter(c.when, payload.trial.to_dict())
        )
        if not conditions:
            logger.debug(f"{LOG_PREFIX} There are no matched conditions")
            return payload

        tags: TList[str] = conditions.reduce(lambda t, x: t + TList([payload.trial.str_format(x.tag)]), payload.trial.tags)
        return DidChallengeAddOnPayload.from_dict({
            "trial": Trial.from_dict({
                "seq": payload.trial.seq,
                "name": payload.trial.name,
                "tags": tags,
                "headers": payload.trial.headers,
                "queries": payload.trial.queries,
                "one": payload.trial.one,
                "other": payload.trial.other,
                "path": payload.trial.path,
                "request_time": payload.trial.request_time,
                "status": payload.trial.status,
                "diff_keys": payload.trial.diff_keys,
            })
        })
