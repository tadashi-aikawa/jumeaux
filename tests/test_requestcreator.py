#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest
from modules import requestcreator
from modules.requestcreator import Format


class TestFromFormat:
    @classmethod
    def teardown_class(cls):
        os.path.exists('tmp') and os.remove('tmp')

    def test_plain(self):
        examinee = """
/path1?a=1&b=2
/path2?c=1

/path3
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = requestcreator.from_format('tmp', Format.PLAIN)

        # Line break is ignored. (examinee has 3 not 4)
        expected = [
            {
                "path": "/path1",
                "qs": {
                    "a": ["1"],
                    "b": ["2"]
                },
                "headers": {}
            },
            {
                "path": "/path2",
                "qs": {
                    "c": ["1"]
                },
                "headers": {}
            },
            {
                "path": "/path3",
                "qs": {},
                "headers": {}
            }
        ]

        assert actual.to_dicts() == expected

    def test_apache(self):
        examinee = """
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test2 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test3?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test4?q1=1&q2=2&q1=3 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = requestcreator.from_format('tmp', Format.APACHE)

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
            requestcreator.from_format('tmp', Format.APACHE)

    def test_yaml(self):
        examinee = """
- path: "/test1"
- path: "/test2"
  qs:
    q1:
      - "1"
- path: "/test3"
  qs:
    q1:
      - "1"
    q2:
      - "2-1"
      - "2-2"
- path: "/test4"
  headers:
    key1: "header1"
    key2: "header2"
- path: "/test5"
  qs:
    q1:
      - "1"
    q2:
      - "2-1"
      - "2-2"
  headers:
    key1: "header1"
    key2: "header2"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = requestcreator.from_format('tmp', Format.YAML)

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
            requestcreator.from_format('tmp', Format.YAML)

    def test_csv(self):
        examinee = """
"/test1","q1=1&q2=2","header1=1&header2=2"
"/test2","q1=1"
"/test3",,"header1=1&header2=2"
"/test4"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        actual = requestcreator.from_format('tmp', Format.CSV)

        expected = [
            {
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
                "path": "/test2",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {}
            },
            {
                "path": "/test3",
                "qs": {},
                "headers": {
                    "header1": "1",
                    "header2": "2"
                }
            },
            {
                "path": "/test4",
                "qs": {},
                "headers": {}
            }
        ]

        assert actual.to_dicts() == expected

    def test_csv_length_over_4(self):
        examinee = """
"/path","q1=1","header1=1","evil"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with pytest.raises(ValueError):
            requestcreator.from_format('tmp', Format.CSV)
