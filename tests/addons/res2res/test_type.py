#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.res2res.type import Executor
from jumeaux.models import Res2ResAddOnPayload, Response


def make_response(type: str, status_code: int) -> Response:
    return Response.from_dict({
        "body": b'{"body": true}',
        "type": type,
        "encoding": "utf-8",
        "headers": {
            "content-type": "application/json"
        },
        "url": "http://test",
        "status_code": status_code,
        "elapsed": datetime.timedelta(seconds=1),
        "elapsed_sec": 1.0,
    })


CHANGE_IF_CONDITION_RES_IS_FULFILLED = (
    "Change if condition(res) is fulfilled.",
    """
    conditions:
      - type: unexpected_type
        when: res.status_code == 201
      - type: expected_type
        when: res.status_code == 200
    """,
    {
        'req': {
            "path": "/path",
            "qs": {},
            "headers": {},
        },
        'response': {
            "body": b'{"body": true}',
            "type": "expected_type",
            "encoding": "utf-8",
            "headers": {
                "content-type": "application/json"
            },
            "url": "http://test",
            "status_code": 200,
            "elapsed": datetime.timedelta(seconds=1),
            "elapsed_sec": 1.0,
        }
    }
)


CHANGE_IF_CONDITION_REQ_IS_FULFILLED = (
    "Change if condition(req) is fulfilled.",
    """
    conditions:
      - type: unexpected_type
        when: req.path == 'hoge'
      - type: expected_type
        when: req.path == '/path'
    """,
    {
        'req': {
            "path": "/path",
            "qs": {},
            "headers": {},
        },
        'response': {
            "body": b'{"body": true}',
            "type": "expected_type",
            "encoding": "utf-8",
            "headers": {
                "content-type": "application/json"
            },
            "url": "http://test",
            "status_code": 200,
            "elapsed": datetime.timedelta(seconds=1),
            "elapsed_sec": 1.0,
        }
    }
)


CHANGE_ONLY_FIST_ONE_IF_CONDITION_IS_FULFILLED = (
    "Change only first one if condition is fulfilled.",
    """
    conditions:
      - type: expected_type
        when: res.status_code == 200
      - type: unexpected_type
        when: res.status_code == 200
    """,
    {
        'req': {
            "path": "/path",
            "qs": {},
            "headers": {},
        },
        'response': {
            "body": b'{"body": true}',
            "type": "expected_type",
            "encoding": "utf-8",
            "headers": {
                "content-type": "application/json"
            },
            "url": "http://test",
            "status_code": 200,
            "elapsed": datetime.timedelta(seconds=1),
            "elapsed_sec": 1.0,
        }
    }
)


NOT_CHANGE_IF_CONDITION_IS_NOT_FULFILLED = (
    "Not change If response status code is 200",
    """
    conditions:
      - type: unexpected_type
        when: res.status_code == 201
    """,
    {
        'req': {
            "path": "/path",
            "qs": {},
            "headers": {},
        },
        'response': {
            "body": b'{"body": true}',
            "type": "json",
            "encoding": "utf-8",
            "headers": {
                "content-type": "application/json"
            },
            "url": "http://test",
            "status_code": 200,
            "elapsed": datetime.timedelta(seconds=1),
            "elapsed_sec": 1.0,
        }
    }
)


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, expected', [
            CHANGE_IF_CONDITION_RES_IS_FULFILLED,
            CHANGE_IF_CONDITION_REQ_IS_FULFILLED,
            CHANGE_ONLY_FIST_ONE_IF_CONDITION_IS_FULFILLED,
            NOT_CHANGE_IF_CONDITION_IS_NOT_FULFILLED,
        ]
    )
    def test_normal(self, title, config_yml, expected):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response("json", 200),
            'req': {
                "path": "/path",
                "qs": {},
                "headers": {},
            }
        })

        assert expected == Executor(load_yaml(config_yml)).exec(payload).to_dict()
