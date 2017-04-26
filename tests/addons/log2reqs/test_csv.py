#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest

from jumeaux.addons.log2reqs.csv import Executor
from jumeaux.models import Log2ReqsAddOnPayload


class TestExec:
    @classmethod
    def teardown_class(cls):
        os.path.exists('tmp') and os.remove('tmp')

    def test_csv(self):
        examinee = """
"name1","/test1","q1=1&q2=2","header1=1&header2=2"
"name2","/test2","q1=1"
"name3","/test3",,"header1=1&header2=2"
"name4","/test4"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))

        expected = [
            {
                "name": "name1",
                "path": "/test1",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "name": "name2",
                "path": "/test2",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {}
            },
            {
                "name": "name3",
                "path": "/test3",
                "qs": {},
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "name": "name4",
                "path": "/test4",
                "qs": {},
                "headers": {}
            }
        ]

        assert actual.to_dicts() == expected

    def test_tsv(self):
        examinee = """
"name1"	"/test1"	"q1=1&q2=2"	"header1=1&header2=2"
"name2"	"/test2"	"q1=1"
"name3"	"/test3"		"header1=1&header2=2"
"name4"	"/test4"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = Executor({"encoding": "utf8", "dialect": 'excel-tab'})\
            .exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))

        expected = [
            {
                "name": "name1",
                "path": "/test1",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "name": "name2",
                "path": "/test2",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {}
            },
            {
                "name": "name3",
                "path": "/test3",
                "qs": {},
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "name": "name4",
                "path": "/test4",
                "qs": {},
                "headers": {}
            }
        ]

        assert actual.to_dicts() == expected

    def test_length_over_5(self):
        examinee = """
"name","/path","q1=1","header1=1","evil"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with pytest.raises(ValueError):
            Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))
