#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from modules import requestcreator


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_from_format_as_wrong_format(self):
        with self.assertRaises(ValueError):
            requestcreator.from_format(None, 'unsupported format')

    def test_from_format_as_apache_normal(self):
        examinee = """
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test2 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test3?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test4?q1=1&q2=2&q1=3 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'apache')

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

        self.assertEqual(actual, expected)

    def test_from_format_as_apache_abnormal_wrong_url_two_questions(self):
        examinee = """
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test?test? HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()

        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            with self.assertRaises(ValueError):
                requestcreator.from_format(f, 'apache')

    def test_from_format_as_yaml_normal(self):
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
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'yaml')

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

        self.assertEqual(actual, expected)

    def test_from_format_as_yaml_abnormal_path_not_exist(self):
        examinee = """
- qs: ""
""".strip()

        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            with self.assertRaises(ValueError):
                requestcreator.from_format(f, 'yaml')

    def test_from_format_as_csv_normal(self):
        examinee = """
"/test1","q1=1&q2=2","header1=1&header2=2"
"/test2","q1=1"
"/test3",,"header1=1&header2=2"
"/test4"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'csv')

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

        self.assertEqual(actual, expected)

    def test_from_format_as_csv_abnormal_length_over_4(self):
        examinee = """
"/path","q1=1","header1=1","evil"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            with self.assertRaises(ValueError):
                requestcreator.from_format(f, 'csv')


if __name__ == '__main__':
    unittest.main()
