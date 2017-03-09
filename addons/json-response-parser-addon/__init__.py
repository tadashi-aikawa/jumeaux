# -*- coding:utf-8 -*-

import json
from owlmixin import OwlMixin
from modules.models import ResponseAddOnPayload


class Config(OwlMixin):
    def __init__(self, force=False):
        self.force: bool = force


def main(payload: ResponseAddOnPayload, config_dict: dict):
    config: Config = Config.from_dict(config_dict or {})
    mime_type = payload.response.headers.get('content-type').split(';')[0]

    return ResponseAddOnPayload.from_dict({
        "response": payload.response,
        "body": json.dumps(
            json.loads(payload.body.decode(payload.encoding)),
            ensure_ascii=False, indent=4, sort_keys=True
        ).encode(payload.encoding) if config.force or mime_type in ('text/json', 'application/json') else payload.body,
        "encoding": payload.encoding
    })
