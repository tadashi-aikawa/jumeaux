#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import shutil
from unittest.mock import MagicMock
from unittest.mock import patch

import os
from requests.exceptions import ConnectionError

from jumeaux import executor
from jumeaux.addons import AddOnExecutor
from jumeaux.models import *


class ResponseBuilder():
    """
    Create mock of requests.models.Response.
    """

    def __init__(self):
        self._text = None
        self._json = None
        self._url = None
        self._status_code = None
        self._content_type = None
        self._content = None
        self._encoding = None
        self._seconds = None
        self._microseconds = None

    def text(self, text):
        self._text = text
        return self

    def json(self, json):
        self._json = json
        return self

    def url(self, url):
        self._url = url
        return self

    def status_code(self, status_code):
        self._status_code = status_code
        return self

    def content_type(self, content_type):
        self._content_type = content_type
        return self

    def content(self, content):
        self._content = content
        return self

    def encoding(self, encoding):
        self._encoding = encoding
        return self

    def second(self, seconds, microseconds):
        self._seconds = seconds
        self._microseconds = microseconds
        return self

    def build(self):
        m = MagicMock()
        m.text = self._text
        m.url = self._url
        m.status_code = self._status_code
        m.headers = {
            "content-type": self._content_type
        }
        m.content = self._content
        m.encoding = self._encoding
        m.elapsed.seconds = self._seconds
        m.elapsed.microseconds = self._microseconds
        m.json.return_value = self._json
        return m


@patch('jumeaux.executor.now')
@patch('jumeaux.executor.concurrent_request')
class TestChallenge:
    """
    Only make mock for jumeaux.concurrent_request.
    Because it uses http requests.
    """

    @classmethod
    def setup_class(cls):
        os.makedirs(os.path.join("tmpdir", "hash_key", "one"))
        os.makedirs(os.path.join("tmpdir", "hash_key", "other"))
        executor.global_addon_executor = AddOnExecutor(Addons.from_dict({
            'log2reqs': {'name': 'jumeaux.addons.log2reqs.csv'}
        }))

    @classmethod
    def teardown_class(cls):
        shutil.rmtree("tmpdir")

    def test_different(self, concurrent_request, now):
        res_one = ResponseBuilder().text('{"items": [1, 2, 3]}') \
            .json({"items": [1, 2, 3]}) \
            .url('URL_ONE') \
            .status_code(200) \
            .content_type('application/json;utf-8') \
            .content(b'{"items": [1, 2, 3]}') \
            .encoding('utf8') \
            .second(1, 234567) \
            .build()

        res_other = ResponseBuilder().text('{"items": [1, 2, 3, 4]}') \
            .json({"items": [1, 2, 3, 4]}) \
            .url('URL_OTHER') \
            .status_code(400) \
            .content_type('application/json;utf-8') \
            .content(b'{"items": [1, 2, 3, 4]}') \
            .encoding('utf8') \
            .second(9, 876543) \
            .build()
        concurrent_request.return_value = res_one, res_other
        now.return_value = datetime.datetime(2000, 1, 1, 0, 0, 0)

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,
            "name": "name1",
            "number_of_request": 10,
            "key": "hash_key",
            "session": None,
            "host_one": None,
            "host_other": None,
            "path": "/challenge",
            "res_dir": "tmpdir",
            "qs": {
                "q1": ["1"],
                "q2": ["2-1", "2-2"]
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "proxy_one": None,
            "proxy_other": None,
            "interval_sec": 0
        })

        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name1",
            "request_time": '2000/01/01 00:00:00',
            "status": Status.DIFFERENT,
            "path": '/challenge',
            "queries": {
                "q1": ["1"],
                "q2": ["2-1", "2-2"]
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "one": {
                "file": "one/(1)name1",
                "url": 'URL_ONE',
                "status_code": 200,
                "byte": 20,
                "response_sec": 1.23,
                "content_type": 'application/json;utf-8',
                'encoding': 'utf8'
            },
            "other": {
                "file": "other/(1)name1",
                "url": 'URL_OTHER',
                "status_code": 400,
                "byte": 23,
                "response_sec": 9.88,
                "content_type": 'application/json;utf-8',
                'encoding': 'utf8'
            }
        }

        assert actual.to_dict() == expected

    def test_same(self, concurrent_request, now):
        res_one = ResponseBuilder().text('a') \
            .url('URL_ONE') \
            .status_code(200) \
            .content_type('text/plain;utf-8') \
            .content(b'a') \
            .encoding('utf8') \
            .second(1, 234567) \
            .build()

        res_other = ResponseBuilder().text('a') \
            .url('URL_OTHER') \
            .status_code(200) \
            .content_type('text/plain') \
            .content(b'a') \
            .encoding('utf8') \
            .second(9, 876543) \
            .build()
        concurrent_request.return_value = res_one, res_other
        now.return_value = datetime.datetime(2000, 1, 1, 0, 0, 0)

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,
            "name": "name2",
            "number_of_request": 10,
            "key": "hash_key",
            "session": None,
            "host_one": None,
            "host_other": None,
            "path": "/challenge",
            "res_dir": "tmpdir",
            "qs": {
                "q1": ["1"],
                "q2": ["2-1", "2-2"]
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "proxy_one": None,
            "proxy_other": None,
            "interval_sec": 0
        })
        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name2",
            "request_time": '2000/01/01 00:00:00',
            "status": Status.SAME,
            "path": '/challenge',
            "queries": {
                'q1': ['1'],
                'q2': ['2-1', '2-2']
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "one": {
                "url": 'URL_ONE',
                "status_code": 200,
                "byte": 1,
                "response_sec": 1.23,
                "content_type": 'text/plain;utf-8',
                'encoding': 'utf8'
            },
            "other": {
                "url": 'URL_OTHER',
                "status_code": 200,
                "byte": 1,
                "response_sec": 9.88,
                "content_type": 'text/plain',
                'encoding': 'utf8'
            }
        }

        assert actual.to_dict() == expected

    def test_failure(self, concurrent_request, now):
        concurrent_request.side_effect = ConnectionError
        now.return_value = datetime.datetime(2000, 1, 1, 0, 0, 0)

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,
            "name": "name3",
            "number_of_request": 10,
            "key": "hash_key",
            "session": None,
            "host_one": "http://one",
            "host_other": "http://other",
            "path": "/challenge",
            "res_dir": "tmpdir",
            "qs": {
                "q1": ["1"]
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "proxy_one": None,
            "proxy_other": None,
            "interval_sec": 0
        })
        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name3",
            "request_time": '2000/01/01 00:00:00',
            "status": Status.FAILURE,
            "path": '/challenge',
            "queries": {
                'q1': ['1']
            },
            "headers": {
                "header1": "1",
                "header2": "2",
            },
            "one": {
                "url": 'http://one/challenge?q1=1',
            },
            "other": {
                "url": 'http://other/challenge?q1=1',
            }
        }

        assert actual.to_dict() == expected


class TestCreateConfig:

    def test(self):
        actual: Config = executor.create_config("tests/config.yaml")
        expected = {
            "base": "base_config.yaml",
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "responses"
            },
            "threads": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2dict": [],
                "judgement": [],
                "dump": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

    def test_no_base(self):
        actual: Config = executor.create_config("tests/config_no_base.yaml")

        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "responses"
            },
            "threads": 1
        }

        assert actual.to_dict() == expected


@patch('jumeaux.executor.now')
@patch('jumeaux.executor.challenge')
@patch('jumeaux.executor.hash_from_args')
class TestExec:
    @classmethod
    def setup_class(cls):
        os.makedirs(os.path.join("tmpdir", "hash_key", "one"))
        os.makedirs(os.path.join("tmpdir", "hash_key", "other"))

    @classmethod
    def teardown_class(cls):
        shutil.rmtree("tmpdir")

    def test(self, hash_from_args, challenge, now):
        DUMMY_HASH = "dummy hash"

        hash_from_args.return_value = DUMMY_HASH
        challenge.side_effect = Trial.from_dicts([
            {
                "seq": 1,
                "name": "name1",
                "request_time": '2000/01/01 00:00:01',
                "status": 'different',
                "path": '/challenge1',
                "queries": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2",
                },
                "one": {
                    "file": "one/(1)name1",
                    "url": 'URL_ONE',
                    "status_code": 200,
                    "byte": 20,
                    "response_sec": 1.23,
                    "content_type": 'application/json; charset=sjis',
                    "encoding": "sjis"
                },
                "other": {
                    "file": "other/(1)name1",
                    "url": 'URL_OTHER',
                    "status_code": 400,
                    "byte": 23,
                    "response_sec": 9.88,
                    "content_type": 'application/json; charset=utf8',
                    "encoding": "utf8"
                }
            },
            {
                "seq": 2,
                "name": "name2",
                "request_time": '2000/01/01 00:00:02',
                "status": 'same',
                "path": '/challenge2',
                "queries": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2",
                },
                "one": {
                    "file": "one/(2)name2",
                    "url": 'URL_ONE',
                    "status_code": 200,
                    "byte": 1,
                    "response_sec": 1.00
                },
                "other": {
                    "file": "other/(2)name2",
                    "url": 'URL_OTHER',
                    "status_code": 200,
                    "byte": 1,
                    "response_sec": 2.00
                }
            }
        ])
        now.side_effect = [
            datetime.datetime(2000, 1, 1, 23, 50, 30),
            datetime.datetime(2000, 1, 2, 0, 0, 0)
        ]

        args: Args = Args.from_dict({
            "files": ['line1', 'line2'],
            "threads": 1,
            "title": "Report title",
            "interval_sec": 0,
            "config": "tests/config.yaml",
            "retry": False,
            "report": None
        })
        config: Config = Config.from_dict({
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "tmpdir"
            },
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "config": {
                        "encoding": "utf8"
                    }
                }
            }
        })
        reqs: TList[Request] = Request.from_dicts([
            {"path": "/dummy"},
            {"path": "/dummy"}
        ])

        actual: Report = executor.exec(args, config, reqs, DUMMY_HASH, None)

        expected = {
            "key": DUMMY_HASH,
            "title": "Report title",
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2dict": [],
                "judgement": [],
                "dump": [],
                "final": []
            },
            "summary": {
                "time": {
                    "start": '2000/01/01 23:50:30',
                    "end": '2000/01/02 00:00:00',
                    "elapsed_sec": 570
                },
                "one": {
                    "host": "http://host/one",
                    "proxy": "http://proxy",
                    "name": "name_one"
                },
                "other": {
                    "host": "http://host/other",
                    "name": "name_other"
                },
                "paths": {
                    "/challenge1": 1,
                    "/challenge2": 1
                },
                "status": {
                    "same": 1,
                    "different": 1,
                    "failure": 0
                },
                "output": {
                    "encoding": "utf8",
                    "response_dir": "tmpdir"
                }
            },
            "trials": [
                {
                    "seq": 1,
                    "name": "name1",
                    "request_time": '2000/01/01 00:00:01',
                    "status": Status.DIFFERENT,
                    "path": '/challenge1',
                    "queries": {
                        "q1": ["1"],
                        "q2": ["2-1", "2-2"]
                    },
                    "headers": {
                        "header1": "1",
                        "header2": "2",
                    },
                    "one": {
                        "file": "one/(1)name1",
                        "url": 'URL_ONE',
                        "status_code": 200,
                        "byte": 20,
                        "response_sec": 1.23,
                        "content_type": 'application/json; charset=sjis',
                        "encoding": "sjis"
                    },
                    "other": {
                        "file": "other/(1)name1",
                        "url": 'URL_OTHER',
                        "status_code": 400,
                        "byte": 23,
                        "response_sec": 9.88,
                        "content_type": 'application/json; charset=utf8',
                        "encoding": "utf8"
                    }
                },
                {
                    "seq": 2,
                    "name": "name2",
                    "request_time": '2000/01/01 00:00:02',
                    "status": Status.SAME,
                    "path": '/challenge2',
                    "queries": {
                        "q1": ["1"],
                        "q2": ["2-1", "2-2"]
                    },
                    "headers": {
                        "header1": "1",
                        "header2": "2",
                    },
                    "one": {
                        "file": "one/(2)name2",
                        "url": 'URL_ONE',
                        "status_code": 200,
                        "byte": 1,
                        "response_sec": 1.00
                    },
                    "other": {
                        "file": "other/(2)name2",
                        "url": 'URL_OTHER',
                        "status_code": 200,
                        "byte": 1,
                        "response_sec": 2.00
                    }
                }
            ]
        }

        assert actual.to_dict() == expected
