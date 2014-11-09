#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from unittest.mock import MagicMock

import gemini
import datetime


class ResponseBuilder():
    """
    Create mock of requests.models.Response.
    """
    def __init__(self):
        self._url = None
        self._status_code = None
        self._content = None
        self._seconds = None
        self._microseconds = None

    def url(self, url):
        self._url = url
        return self

    def status_code(self, status_code):
        self._status_code = status_code
        return self

    def content(self, content):
        self._content = content
        return self

    def second(self, seconds, microseconds):
        self._seconds = seconds
        self._microseconds = microseconds
        return self

    def build(self):
        m = MagicMock()
        m.url = self._url
        m.status_code = self._status_code
        m.content = self._content
        m.elapsed.seconds = self._seconds
        m.elapsed.microseconds = self._microseconds
        return m


class CreateProxiesTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        proxy = '1.2.3.4'
        actual = gemini.create_proxies(proxy)

        self.assertEqual(actual['http'], 'http://1.2.3.4')
        self.assertEqual(actual['https'], 'https://1.2.3.4')

    def test_None(self):
        proxy = None
        actual = gemini.create_proxies(proxy)

        self.assertEqual(actual, {})


class CreateTrialTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        self.maxDiff = None

        status = 'status'
        req_time = datetime.datetime(2000, 1, 2, 0, 10, 20, 123456)
        path = '/path'
        qs = 'q1=1&q2=10000&q2=2'
        res_one = ResponseBuilder().url('URL_ONE') \
                                   .status_code(200) \
                                   .content('a') \
                                   .second(1, 234567) \
                                   .build()
        res_other = ResponseBuilder().url('URL_OTHER') \
                                     .status_code(400) \
                                     .content('ab') \
                                     .second(9, 876543) \
                                     .build()

        actual = gemini.create_trial(res_one, res_other, status, req_time, path, qs)
        expected = {
            "request_time": '2000/01/02 00:10:20',
            "status": 'status',
            "path": '/path',
            "queries": {
                'q1': ['1'],
                'q2': ['10000', '2']
            },
            "one": {
                "url": 'URL_ONE',
                "status_code": 200,
                "byte": 1,
                "response_sec": 1.23
            },
            "other": {
                "url": 'URL_OTHER',
                "status_code": 400,
                "byte": 2,
                "response_sec": 9.88
            }
        }

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
