#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2res.json import Executor
from jumeaux.models import Res2ResAddOnPayload, Response

TEXT = json.dumps({
    "id": 1,
    "name": "山田Ichiro"
})


def make_response(text: str, encoding: str, body_encoding: str) -> Response:
    return Response.from_dict({
        "body": text.encode(body_encoding),
        "encoding": encoding,
        "headers": {
            "content-type": "application/json"
        },
        "url": "http://test",
        "status_code": 200,
        "elapsed": datetime.timedelta(seconds=1)
    })


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, expected_text', [
            (
                "Normal",
                """
                transformer:
                  module: jumeaux.addons.res2res.json
                  function: wrap
                """,
                {
                    "wrap": {
                        "id": 1,
                        "name": "山田Ichiro"
                    }
                }
            ),
        ]
    )
    def test_normal(self, title, config_yml, expected_text):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response(TEXT, 'utf-8', 'utf-8'),
            'req': {
                "path": "/path",
                "qs": {},
                "headers": {},
            }
        })

        expected = {
            'response': make_response(json.dumps(expected_text, ensure_ascii=False), 'utf-8', 'utf-8').to_dict(),
            'req': {
                "path": "/path",
                "qs": {},
                "headers": {},
            }
        }

        assert expected == Executor(load_yaml(config_yml)).exec(payload).to_dict()

    @pytest.mark.parametrize(
        'title, config_yml', [
            (
                "Invalid module",
                """
                transformer:
                  module: jumeaux.addons.res2res.invalid
                  function: invalid
                """
            ),
            (
                "Invalid function",
                """
                transformer:
                  module: jumeaux.addons.res2res.json
                  function: invalid
                """
            ),
        ]
    )
    def test_error(self, title, config_yml):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response(TEXT, 'utf-8', 'utf-8'),
            'req': {
                "path": "/path",
                "qs": {},
                "headers": {},
            }
        })

        with pytest.raises(SystemExit):
            Executor(load_yaml(config_yml)).exec(payload)
