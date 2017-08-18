#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest

from jumeaux.addons.conditions import RequestCondition
from jumeaux.models import Request


class TestRequestCondition:
    @pytest.mark.parametrize(
        'expected, req', [
            (True, {"name": "This is OK", "path": "/valid"}),
            (False, {"name": "This is NG", "path": "/valid"}),
            (False, {"name": "This is OK or NG?", "path": "/valid"}),
            (False, {"name": "This is OK but invalid", "path": "/invalid"}),
        ]
    )
    def test_all_and(self, expected, req):
        condition: RequestCondition = RequestCondition.from_dict({
            "name": {
                "items": [
                    {"regexp": ".*OK.*"},
                    {"regexp": ".*NG.*", "negative": True},
                ],
                "and_or": "and"
            },
            "path": {
                "items": [
                    {"regexp": "/valid"},
                ],
                "and_or": "and"
            },
            "and_or": "and"
        })

        assert condition.fulfill(Request.from_dict(req)) is expected

    @pytest.mark.parametrize(
        'expected, req', [
            (True, {"name": "This is OK", "path": "/valid"}),
            (False, {"name": "This is NG", "path": "/valid"}),
            (True, {"name": "This is OK or NG?", "path": "/valid"}),
            (False, {"name": "This is OK but invalid", "path": "/invalid"}),
        ]
    )
    def test_matchers_are_or(self, expected, req):
        condition: RequestCondition = RequestCondition.from_dict({
            "name": {
                "items": [
                    {"regexp": ".*OK.*"},
                    {"regexp": ".*NG.*", "negative": True},
                ],
                "and_or": "or"
            },
            "path": {
                "items": [
                    {"regexp": "/valid"},
                ],
                "and_or": "or"
            },
            "and_or": "and"
        })

        assert condition.fulfill(Request.from_dict(req)) is expected

    @pytest.mark.parametrize(
        'expected, req', [
            (True, {"name": "This is OK", "path": "/valid"}),
            (True, {"name": "This is NG", "path": "/valid"}),
            (True, {"name": "This is OK or NG?", "path": "/valid"}),
            (True, {"name": "This is OK but invalid", "path": "/invalid"}),
        ]
    )
    def test_all_or(self, expected, req):
        condition: RequestCondition = RequestCondition.from_dict({
            "name": {
                "items": [
                    {"regexp": ".*OK.*"},
                    {"regexp": ".*NG.*", "negative": True},
                ],
                "and_or": "or"
            },
            "path": {
                "items": [
                    {"regexp": "/valid"},
                ],
                "and_or": "or"
            },
            "and_or": "or"
        })

        assert condition.fulfill(Request.from_dict(req)) is expected
