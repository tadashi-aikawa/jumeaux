#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.store_criterion.free import Executor
from jumeaux.models import StoreCriterionAddOnPayload, Response, StoreCriterionAddOnReference, CaseInsensitiveDict

EMPTY_KEYS = {
    'changed': [], 'added': [], 'removed': []
}

RES_ONE = Response.from_dict({
    'body': b'a',
    "type": "unknown",
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=1),
    "elapsed_sec": 1.0,
})

RES_OTHER = Response.from_dict({
    'body': b'b',
    "type": "unknown",
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=2),
    "elapsed_sec": 2.0,
})

REFERENCE = {
    'status': 'same',
    'name': 'no title',
    'req': {
        'path': '/test1',
        'qs': {},
        'headers': {},
    },
    'res_one': RES_ONE,
    'res_other': RES_OTHER,
}


class TestExec:
    @pytest.mark.parametrize(
        'title, payload, config, expected', [
            (
                "Match 1 of 1",
                {'stored': False},
                """
                when_any:
                  - status == "same"
                """,
                {'stored': True},
            ),
            (
                "Match 0 of 1",
                {'stored': False},
                """
                when_any:
                  - status == 'different'
                """,
                {'stored': False},
            ),
            (
                "Match 1 of 2",
                {'stored': False},
                """
                when_any:
                  - status == 'different'
                  - status == 'same'
                """,
                {'stored': True},
            ),
            (
                "Match 2 of 3",
                {'stored': False},
                """
                when_any:
                  - req.path == '/test0'
                  - req.path == '/test1'
                  - status == 'same'
                """,
                {'stored': True},
            ),
            (
                "No config",
                {'stored': False},
                """
                """,
                {'stored': True},
            ),
        ]
    )
    def test(self, title, payload, config, expected):
        actual: StoreCriterionAddOnPayload = Executor(load_yaml(config)).exec(
            StoreCriterionAddOnPayload.from_dict(payload),
            StoreCriterionAddOnReference.from_dict(REFERENCE),
        )
        assert expected == actual.to_dict()


