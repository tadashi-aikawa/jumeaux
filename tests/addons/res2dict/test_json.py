#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2dict.json import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

NORMAL_BODY = json.dumps({
    "total": 10,
    "items": [
        {"id": 1, "name": "Ichiro", "favorites": ["apple", "orange"]},
        {"id": 2, "name": "Jiro"}
    ]
})


NORMAL_CASE = ("Normal",
    """
    force: False 
    """,
    Response.from_dict({
        "body": NORMAL_BODY.encode('utf-8'),
        "encoding": 'utf-8',
        "text": NORMAL_BODY,
        "headers": {
            "content-type": "application/json"
        },
        "url": "http://test",
        "status_code": 200,
        "elapsed": datetime.timedelta(seconds=1)
    }),
    {
        "total": 10,
        "items": [
            {
                "id": 1,
                "name": "Ichiro",
                "favorites": ["apple", "orange"]
            },
            {
                "id": 2,
                "name": "Jiro"
            }
        ]
    }
)

EMPTY_ENCODING_CASE = ("Encoding is empty",
    """
    force: False 
    """,
    Response.from_dict({
        "body": NORMAL_BODY.encode('utf-8'),
        "text": NORMAL_BODY,
        "headers": {
            "content-type": "application/json"
        },
        "url": "http://test",
        "status_code": 200,
        "elapsed": datetime.timedelta(seconds=1)
    }),
    {
        "total": 10,
        "items": [
            {
                "id": 1,
                "name": "Ichiro",
                "favorites": ["apple", "orange"]
            },
            {
                "id": 2,
                "name": "Jiro"
            }
        ]
    }
)


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, expected_result', [
            NORMAL_CASE, EMPTY_ENCODING_CASE
        ]
    )
    def test(self, title, config_yml, response, expected_result):
        payload: Res2DictAddOnPayload = Res2DictAddOnPayload.from_dict({
            'response': response,
        })

        actual: Res2DictAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert actual.response == response
        assert actual.result.get() == expected_result
