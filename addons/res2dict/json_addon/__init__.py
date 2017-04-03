# -*- coding:utf-8 -*-

import json
from typing import Optional
from owlmixin import OwlMixin
from modules.models import Res2DictAddOnPayload


class Config(OwlMixin):
    def __init__(self, force=False, force_encoding=None):
        self.force: bool = force
        self.force_encoding: Optional[str] = force_encoding


def exec(payload: Res2DictAddOnPayload, config_dict: dict):
    config: Config = Config.from_dict(config_dict or {})
    if payload.result and not config.force:
        return payload

    mime_type = payload.response.headers.get('content-type').split(';')[0]
    encoding = config.force_encoding or payload.response.encoding

    return Res2DictAddOnPayload.from_dict({
        "response": payload.response,
        "result": json.loads(payload.response.text, encoding=encoding) \
            if config.force or mime_type in ('text/json', 'application/json') \
            else None
    })
