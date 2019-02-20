#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from owlmixin.util import load_yaml
from jumeaux.addons.judgement.ignore import Executor
from jumeaux.models import JudgementAddOnPayload, Response, CaseInsensitiveDict, JudgementAddOnReference

CONFIG = load_yaml(r"""
ignores:
  - title: Check point 1
    conditions:
      - when: '"/test1" in path'
        added:
          - path: root<'add'><[0-1]>
          - path: root<'add'><2>
      - when: '"/test2" in path and name == "no title"'
        changed:
          - path: root<'change'><[0-1]>
          - path: root<'change'><2>
        removed:
          - path: root<'remove'><[0-1]>
          - path: root<'remove'><2>
      - added:
          - path: root<'add'><3>
  - title: Check point 2
    conditions:
      - added:
          - path: root<'add'><99>
  - title: Check point 3
    conditions:
      - when: '"value_when" in qs and qs["value_when"][0] == "yes"'
        added:
          - path: root<'add'><[0-1]>
            when: 'other == "ignore"'
      - when: '"value_when" in qs and qs["value_when"][0] == "yes"'
        changed:
          - path: root<'change'><\d+>
            when: 'one == "ignore" and other == "ignore"'
          - path: root<'change'><\d+>
            when: '"IGNORE" in one'
""")

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

DICT_ONE = {
    'base': 1,
    'change': ["ignore", "IGNORE", "ignore"],
}

DICT_OTHER = {
    'base': 1,
    'add': ["ignore", "not_ignore"],
    'change': ["ignore", "not_ignore", "not_ignore"],
}


class TestExec:
    def test_only_condition_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>"],
                    'changed': [],
                    'removed': []
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>"],
                    'changed': [],
                    'removed': []
                }
            },
            'regard_as_same': True
        } == actual.to_dict()

    def test_only_condition_partial_same_is_false(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0><extra>", "root<'add'><1><extra>", "root<'add'><2><extra>"],
                    'changed': [],
                    'removed': []
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0><extra>", "root<'add'><1><extra>", "root<'add'><2><extra>"],
                    'changed': [],
                    'removed': []
                }
            },
            'regard_as_same': False
        } == actual.to_dict()

    def test_over_conditions_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>"],
                    'changed': [],
                    'removed': [],
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert actual.to_dict() == {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>"],
                    'changed': [],
                    'removed': [],
                }
            },
            'regard_as_same': True
        }

    def test_over_ignores_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>", "root<'add'><99>"],
                    'changed': [],
                    'removed': []
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>"],
                    'changed': [],
                    'removed': []
                },
                'Check point 2': {
                    'added': ["root<'add'><99>"],
                    'changed': [],
                    'removed': []
                }
            },
            'regard_as_same': True
        } == actual.to_dict()

    def test_over_ignores_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>", "root<'add'><4>", "root<'add'><99>"],
                    'changed': [],
                    'removed': []
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>", "root<'add'><3>"],
                    'changed': [],
                    'removed': []
                },
                'Check point 2': {
                    'added': ["root<'add'><99>"],
                    'changed': [],
                    'removed': []
                },
                'unknown': {
                    'added': ["root<'add'><4>"],
                    'changed': [],
                    'removed': []
                }
            },
            'regard_as_same': False
        } == actual.to_dict()

    def test_path_specified_same(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': [],
                    'changed': ["root<'change'><0>", "root<'change'><1>", "root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>", "root<'remove'><2>"]
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': [],
                    'changed': ["root<'change'><0>", "root<'change'><1>", "root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>", "root<'remove'><2>"]
                }
            },
            'regard_as_same': True
        } == actual.to_dict()

    def test_path_specified_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>"],
                    'changed': [],
                    'removed': []
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition':  {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>", "root<'add'><2>"],
                    'changed': [],
                    'removed': []
                }
            },
            'regard_as_same': False
        } == actual.to_dict()

    def test_name_specified_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': [],
                    'changed': ["root<'change'><0>", "root<'change'><1>", "root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>", "root<'remove'><2>"]
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'unknown': {
                    'added': [],
                    'changed': ["root<'change'><0>", "root<'change'><1>", "root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>", "root<'remove'><2>"]
                }
            },
            'regard_as_same': False
        } == actual.to_dict()

    def test_merge_to_default_diffs(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': [],
                    'changed': ["root<'change'><default>"],
                    'removed': ["root<'remove'><default>"]
                },
                'Check point 2': {
                    'added': ["root<'add'><default>"],
                    'changed': [],
                    'removed': [],
                },
                'unknown': {
                    'added': ["root<'add'><0>"],
                    'changed': ["root<'change'><0>"],
                    'removed': ["root<'remove'><0>"]
                }
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
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 1': {
                    'added': [],
                    'changed': ["root<'change'><default>", "root<'change'><0>"],
                    'removed': ["root<'remove'><default>", "root<'remove'><0>"]
                },
                'Check point 2': {
                    'added': ["root<'add'><default>"],
                    'changed': [],
                    'removed': [],
                },
                'unknown': {
                    'added': ["root<'add'><0>"],
                    'changed': [],
                    'removed': [],
                }
            },
            'regard_as_same': False
        } == actual.to_dict()

    def test_value_not_match_different(self):
        payload: JudgementAddOnPayload = JudgementAddOnPayload.from_dict({
            'diffs_by_cognition': {
                'unknown': {
                    'added': ["root<'add'><0>", "root<'add'><1>"],
                    'changed': ["root<'change'><0>", "root<'change'><1>", "root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>"]
                }
            },
            'regard_as_same': False
        })
        reference: JudgementAddOnReference = JudgementAddOnReference.from_dict({
            'name': 'title',
            'path': '/test',
            'qs': {'value_when': ["yes"]},
            'headers': {},
            'res_one': RES_ONE,
            'res_other': RES_OTHER,
            'dict_one': DICT_ONE,
            'dict_other': DICT_OTHER,
        })

        actual: JudgementAddOnPayload = Executor(CONFIG).exec(payload, reference)

        assert {
            'diffs_by_cognition': {
                'Check point 3': {
                    'added': ["root<'add'><0>"],
                    'changed': ["root<'change'><0>", "root<'change'><1>"],
                    'removed': []
                },
                'unknown': {
                    'added': ["root<'add'><1>"],
                    'changed': ["root<'change'><2>"],
                    'removed': ["root<'remove'><0>", "root<'remove'><1>"]
                }
            },
            'regard_as_same': False
        } == actual.to_dict()
