#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from jumeaux.addons.judgement.ignore_properties import Executor
from jumeaux.models import JudgementAddOnPayload, Response, CaseInsensitiveDict, JudgementAddOnReference

CONFIG = {
    'ignores': [
        {
            'title': 'Check point 1',
            'conditions': [
                {
                    'path': '/test1',
                    'added': [
                        '<add><[0-1]>',
                        '<add><2>'
                    ]
                },
                {
                    'path': '/test2',
                    'name': 'no title',
                    'changed': [
                        '<change><[0-1]>',
                        '<change><2>'
                    ],
                    'removed': [
                        '<remove><[0-1]>',
                        '<remove><2>'
                    ]
                },
                {
                    'added': ['<add><3>']
                }
            ]
        },
        {
            'title': 'Check point 2',
            'conditions': [
                {
                    'added': ['<add><99>']
                }
            ]
        }
    ]
}

RES_ONE = Response.from_dict({
    'body': b'a',
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=1)
})

RES_OTHER = Response.from_dict({
    'body': b'b',
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=2)
})


class TestExec:
    def test_only_condition_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False,
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
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
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': [],
                'changed': [],
                'removed': []
            },
            'regard_as_same': True
        }

    def test_only_condition_partial_same_is_false(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0><extra>', '<add><1><extra>', '<add><2><extra>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test1',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': ['<add><0><extra>', '<add><1><extra>', '<add><2><extra>'],
                'changed': [],
                'removed': []
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': ['<add><0><extra>', '<add><1><extra>', '<add><2><extra>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        }

    def test_over_conditions_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test1',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>'],
                'changed': [],
                'removed': []
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': [],
                'changed': [],
                'removed': []
            },
            'regard_as_same': True
        }

    def test_over_ignores_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>', '<add><99>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test1',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>', '<add><99>'],
                'changed': [],
                'removed': []
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': [],
                'changed': [],
                'removed': []
            },
            'regard_as_same': True
        }

    def test_over_ignores_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>', '<add><4>', '<add><99>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test1',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>', '<add><3>', '<add><4>', '<add><99>'],
                'changed': [],
                'removed': []
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': ['<add><4>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        }

    def test_path_specified_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': [],
                'changed': ['<change><0>', '<change><1>', '<change><2>'],
                'removed': ['<remove><0>', '<remove><1>', '<remove><2>']
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test2',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': [],
                'changed': ['<change><0>', '<change><1>', '<change><2>'],
                'removed': ['<remove><0>', '<remove><1>', '<remove><2>']
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': [],
                'changed': [],
                'removed': []
            },
            'regard_as_same': True
        }

    def test_path_specified_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'no title',
            'path': '/test2',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': ['<add><0>', '<add><1>', '<add><2>'],
                'changed': [],
                'removed': []
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys':  {
                'added': ['<add><0>', '<add><1>', '<add><2>'],
                'changed': [],
                'removed': []
            },
            'regard_as_same': False
        }

    def test_name_specified_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'remaining_diff_keys': {
                'added': [],
                'changed': ['<change><0>', '<change><1>', '<change><2>'],
                'removed': ['<remove><0>', '<remove><1>', '<remove><2>']
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'title',
            'path': '/test2',
            'qs': {},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'diff_keys': {
                'added': [],
                'changed': ['<change><0>', '<change><1>', '<change><2>'],
                'removed': ['<remove><0>', '<remove><1>', '<remove><2>']
            },
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'remaining_diff_keys': {
                'added': [],
                'changed': ['<change><0>', '<change><1>', '<change><2>'],
                'removed': ['<remove><0>', '<remove><1>', '<remove><2>']
            },
            'regard_as_same': False
        }
