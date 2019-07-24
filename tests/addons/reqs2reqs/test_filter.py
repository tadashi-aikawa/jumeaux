#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.reqs2reqs.filter import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload

AND = (
    "And filter",
    """
    when: ('ok' in path) and ('OK' in name)
    """,
    [
        {"name": "It's OK", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's OK", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
    ],
    [
        {
            "name": "It's OK",
            "method": "GET",
            "path": "/ok",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        }
    ],
)

OR = (
    "Or filter",
    """
    when: ('ok' in path) or ('OK' in name)
    """,
    [
        {"name": "It's OK", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's OK", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
    ],
    [
        {
            "name": "It's OK",
            "method": "GET",
            "path": "/ok",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
        {
            "name": "It's OK",
            "method": "GET",
            "path": "/ng",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
        {
            "name": "It's NG",
            "method": "GET",
            "path": "/ok",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
    ],
)

NEGATIVE = (
    "Negative filter",
    """
    when: not (('ok' in path) and ('OK' in name))
    """,
    [
        {"name": "It's OK", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's OK", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ok", "headers": {}, "qs": {}},
        {"name": "It's NG", "method": "GET", "path": "/ng", "headers": {}, "qs": {}},
    ],
    [
        {
            "name": "It's OK",
            "method": "GET",
            "path": "/ng",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
        {
            "name": "It's NG",
            "method": "GET",
            "path": "/ok",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
        {
            "name": "It's NG",
            "method": "GET",
            "path": "/ng",
            "headers": {},
            "qs": {},
            "url_encoding": "utf-8",
        },
    ],
)


class TestExec:
    @pytest.mark.parametrize("title, config_yml, requests, expected_result", [AND, OR, NEGATIVE])
    def test_filter(self, title, config_yml, requests, expected_result):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({"requests": requests})

        actual: Reqs2ReqsAddOnPayload = Executor(load_yaml(config_yml)).exec(payload, None)

        assert expected_result == actual.requests.to_dicts()
