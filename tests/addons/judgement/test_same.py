#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.judgement.same import Executor
from jumeaux.models import JudgementAddOnPayload, Response, CaseInsensitiveDict, JudgementAddOnReference

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
    'name': 'no title',
    'path': '/test1',
    'qs': {},
    'headers': {},
    'res_one': RES_ONE,
    'res_other': RES_OTHER,
    'diff_keys': {
        'added': ['<add><0>', '<add><1>', '<add><2>'],
        'changed': [],
        'removed': []
    },
}


class TestExec:
    @pytest.mark.parametrize(
        'title, payload, config, expected', [
            (
                "Match 1 of 1",
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
                """
                when_any:
                  - path == '/test1'
                """,
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': True},
            ),
            (
                "Match 0 of 1",
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
                """
                when_any:
                  - path == '/test0'
                """,
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
            ),
            (
                "Match 1 of 2",
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
                """
                when_any:
                  - path == '/test0'
                  - path == '/test1'
                """,
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': True},
            ),
            (
                "Match 2 of 3",
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
                """
                when_any:
                  - path == '/test1'
                  - path == '/test1'
                  - name == 'no title'
                """,
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': True},
            ),
        ]
    )
    def test(self, title, payload, config, expected):
        actual: JudgementAddOnPayload = Executor(load_yaml(config)).exec(
            JudgementAddOnPayload.from_dict(payload),
            JudgementAddOnReference.from_dict(REFERENCE),
        )
        assert expected == actual.to_dict()

    @pytest.mark.parametrize(
        'title, payload, config', [
            (
                "No config",
                {'remaining_diff_keys': EMPTY_KEYS, 'regard_as_same': False},
                """
                """,
            ),
        ]
    )
    def test_exit(self, title, payload, config):
        with pytest.raises(SystemExit):
            Executor(load_yaml(config)).exec(
                JudgementAddOnPayload.from_dict(payload),
                JudgementAddOnReference.from_dict(REFERENCE),
            )

