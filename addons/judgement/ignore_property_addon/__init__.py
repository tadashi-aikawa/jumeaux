# -*- coding:utf-8 -*-

import json
from typing import Optional
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import JudgementAddOnPayload


class Config(OwlMixin):
    def __init__(self, ignore_properties):
        self.ignore_properties: TList[str] = TList(ignore_properties)


def exec(payload: JudgementAddOnPayload, config_dict: dict):
    if payload.regard_as_same:
        return payload

    config: Config = Config.from_dict(config_dict or {})
    return JudgementAddOnPayload.from_dict({
        "res_one": payload.res_one,
        "res_other": payload.res_other,
        "diff_keys": payload.diff_keys,
        "regard_as_same": payload.diff_keys.removed.all(lambda x: x in config.ignore_properties)
    })
