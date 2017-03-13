#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest
from addons.log.apache_addon import exec


class TestFromFormat:
    @classmethod
    def teardown_class(cls):
        os.path.exists('tmp') and os.remove('tmp')

    def test_apache(self):
        examinee = """
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test2 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test3?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test4?q1=1&q2=2&q1=3 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = exec('tmp', {"encoding": "utf8"})

        expected = [
            {
                "path": "/test1",
                "qs": {},
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "path": "/test2",
                "qs": {},
                "headers": {}
            },
            {
                "path": "/test3",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {}
            },
            {
                "path": "/test4",
                "qs": {
                    "q1": ["1", "3"],
                    "q2": ["2"]
                },
                "headers": {}
            },
        ]

        assert actual.to_dicts() == expected

    def test_apache_wrong_url_two_questions(self):
        examinee = """
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test?test? HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()

        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with pytest.raises(ValueError):
            exec('tmp', {"encoding": "utf8"})
