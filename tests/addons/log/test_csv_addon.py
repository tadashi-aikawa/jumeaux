#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest
from addons.log.csv_addon import exec


class TestFromFormat:
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
        actual = exec('tmp', {"encoding": "utf8"})

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

    def test_csv_length_over_5(self):
        examinee = """
"name","/path","q1=1","header1=1","evil"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with pytest.raises(ValueError):
            exec('tmp', {"encoding": "utf8"})
