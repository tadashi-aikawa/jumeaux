# -*- coding:utf-8 -*-

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

from jumeaux.addons.judgement import JudgementExecutor
from jumeaux.utils import get_by_diff_key
from jumeaux.logger import Logger
from jumeaux.models import JudgementAddOnPayload, DiffKeys, JudgementAddOnReference

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    values: TList[str]


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: JudgementAddOnPayload, reference: JudgementAddOnReference) -> JudgementAddOnPayload:
        if payload.regard_as_same or payload.remaining_diff_keys.is_none():
            return payload

        def reject_apple(key: str):
            one = get_by_diff_key(reference.dict_one.get(), key)
            other = get_by_diff_key(reference.dict_other.get(), key)
            return self.config.values.any(lambda x: x in str(one) or x in str(other))

        keys: DiffKeys = payload.remaining_diff_keys.get()
        filtered_diff_keys: DiffKeys = DiffKeys.from_dict({
            'added': keys.added.reject(reject_apple),
            'changed': keys.changed.reject(reject_apple),
            'removed': keys.removed.reject(reject_apple),
        })


        return JudgementAddOnPayload.from_dict({
            "remaining_diff_keys": filtered_diff_keys,
            "regard_as_same": not (filtered_diff_keys.added or filtered_diff_keys.removed or filtered_diff_keys.changed)
        })
