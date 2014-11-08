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
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test2 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test3?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test4?q1=1&q2=2 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'apache')

        self.assertEqual(len(actual), 4)

        self.assertEqual(actual[0]['path'], '/test')
        self.assertEqual(actual[0]['qs'], '')
        self.assertEqual(actual[1]['path'], '/test2')
        self.assertEqual(actual[1]['qs'], '')
        self.assertEqual(actual[2]['path'], '/test3')
        self.assertEqual(actual[2]['qs'], 'q1=1')
        self.assertEqual(actual[3]['path'], '/test4')
        self.assertEqual(actual[3]['qs'], 'q1=1&q2=2')

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
- path: "/test"
  qs: ""
- path: "/test2"
- path: "/test3"
  qs: "q1=1"
- path: "/test4"
  qs: "q1=1&q2=2"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'yaml')

        self.assertEqual(len(actual), 4)

        self.assertEqual(actual[0]['path'], '/test')
        self.assertEqual(actual[0]['qs'], '')
        self.assertEqual(actual[1]['path'], '/test2')
        self.assertEqual(actual[1]['qs'], '')
        self.assertEqual(actual[2]['path'], '/test3')
        self.assertEqual(actual[2]['qs'], 'q1=1')
        self.assertEqual(actual[3]['path'], '/test4')
        self.assertEqual(actual[3]['qs'], 'q1=1&q2=2')

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
"/test",
"/test2"
"/test3","q1=1"
"/test4","q1=1&q2=2"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            actual = requestcreator.from_format(f, 'csv')

        self.assertEqual(len(actual), 4)

        self.assertEqual(actual[0]['path'], '/test')
        self.assertEqual(actual[0]['qs'], '')
        self.assertEqual(actual[1]['path'], '/test2')
        self.assertEqual(actual[1]['qs'], '')
        self.assertEqual(actual[2]['path'], '/test3')
        self.assertEqual(actual[2]['qs'], 'q1=1')
        self.assertEqual(actual[3]['path'], '/test4')
        self.assertEqual(actual[3]['qs'], 'q1=1&q2=2')

    def test_from_format_as_csv_abnormal_length_over_3(self):
        examinee = """
"/path","q1=1","evil"
""".strip()
        with open('tmp', 'w', encoding='utf8') as f:
            f.write(examinee)
        with open('tmp', 'r', encoding='utf8') as f:
            with self.assertRaises(ValueError):
                requestcreator.from_format(f, 'csv')


if __name__ == '__main__':
    unittest.main()
