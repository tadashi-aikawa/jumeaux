#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest
from addons.log2reqs.json import Executor
from modules.models import Log2ReqsAddOnPayload


class TestFromFormat:
    @classmethod
    def teardown_class(cls):
        os.path.exists('tmp') and os.remove('tmp')

    def test_json(self):
        examinee = """[
    {
        "path": "/test1"
    },
    {
        "path": "/test2",
        "qs": {
            "q1": ["1"]
        }
    },
    {
        "path": "/test3",
        "qs": {
            "q1": ["1"],
            "q2": ["2-1", "2-2"]
        }
    },
    {
        "path": "/test4",
        "headers": {
            "key1": "header1",
            "key2": "header2"
        }
    },
    {
        "path": "/test5",
        "qs": {
            "q1": ["1"],
            "q2": ["2-1", "2-2"]
        },
        "headers": {
            "key1": "header1",
            "key2": "header2"
        }
    }
]
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))

        expected = [
            {
                "path": "/test1",
                "qs": {},
                "headers": {}
            },
            {
                "path": "/test2",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {}
            },
            {
                "path": "/test3",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {}
            },
            {
                "path": "/test4",
                "qs": {},
                "headers": {
                    "key1": "header1",
                    "key2": "header2"
                }
            },
            {
                "path": "/test5",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {
                    "key1": "header1",
                    "key2": "header2"
                }
            }
        ]

        assert actual.to_dicts() == expected

    def test_yaml_path_not_exist(self):
        examinee = """
- qs: ""
""".strip()

        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with pytest.raises(ValueError):
            Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))
