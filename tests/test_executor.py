#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil
import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from requests.exceptions import ConnectionError
from owlmixin import TList

from jumeaux import executor, __version__
from jumeaux.addons import AddOnExecutor
from jumeaux.executor import merge_args2config
from jumeaux.models import (
    CaseInsensitiveDict,
    Addons,
    ChallengeArg,
    Config,
    Args,
    Request,
    Report,
)


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
        m.headers = CaseInsensitiveDict({
            "content-type": self._content_type
        })
        m.content = self._content
        m.encoding = self._encoding
        m.elapsed = datetime.timedelta(seconds=self._seconds, microseconds=self._microseconds)
        m.json.return_value = self._json
        return m


@patch('jumeaux.executor.store_criterion')
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

    def test_different(self, concurrent_request, now, store_criterion):
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
        now.return_value = datetime.datetime(2000, 1, 1, 10, 10, 10, 10)
        store_criterion.return_value = True

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,

            "number_of_request": 10,
            "key": "hash_key",
            "session": 'dummy',
            "req": {
                "name": "name1",
                "path": "/challenge",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2",
                },
            },
            "host_one": 'hoge_one',
            "host_other": 'hoge_other',
            "res_dir": "tmpdir",
            "proxy_one": None,
            "proxy_other": None
        })

        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name1",
            "request_time": '2000-01-01T10:10:10.000010',
            "status": 'different',
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
                "mime_type": 'application/json',
                'encoding': 'utf8'
            },
            "other": {
                "file": "other/(1)name1",
                "url": 'URL_OTHER',
                "status_code": 400,
                "byte": 23,
                "response_sec": 9.88,
                "content_type": 'application/json;utf-8',
                "mime_type": 'application/json',
                'encoding': 'utf8'
            }
        }

        assert actual == expected

    def test_same(self, concurrent_request, now, store_criterion):
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
        now.return_value = datetime.datetime(2000, 1, 1, 10, 10, 10, 10)
        store_criterion.return_value = False

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,
            "number_of_request": 10,
            "key": "hash_key",
            "session": 'dummy',
            "req": {
                "name": "name2",
                "path": "/challenge",
                "qs": {
                    "q1": ["1"],
                    "q2": ["2-1", "2-2"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2",
                },
            },
            "host_one": 'hoge_one',
            "host_other": 'hoge_other',
            "res_dir": "tmpdir",
            "proxy_one": None,
            "proxy_other": None
        })
        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name2",
            "request_time": '2000-01-01T10:10:10.000010',
            "status": 'same',
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
                "mime_type": 'text/plain',
                'encoding': 'utf8'
            },
            "other": {
                "url": 'URL_OTHER',
                "status_code": 200,
                "byte": 1,
                "response_sec": 9.88,
                "content_type": 'text/plain',
                "mime_type": 'text/plain',
                'encoding': 'utf8'
            }
        }

        assert actual == expected

    def test_failure(self, concurrent_request, now, store_criterion):
        concurrent_request.side_effect = ConnectionError
        now.return_value = datetime.datetime(2000, 1, 1, 10, 10, 10, 10)
        store_criterion.return_value = False

        args: ChallengeArg = ChallengeArg.from_dict({
            "seq": 1,
            "number_of_request": 10,
            "key": "hash_key",
            "session": 'dummy',
            "req": {
                "name": "name3",
                "path": "/challenge",
                "qs": {
                    "q1": ["1"]
                },
                "headers": {
                    "header1": "1",
                    "header2": "2",
                },
            },
            "host_one": "http://one",
            "host_other": "http://other",
            "res_dir": "tmpdir",
            "proxy_one": None,
            "proxy_other": None
        })
        actual = executor.challenge(args)

        expected = {
            "seq": 1,
            "name": "name3",
            "request_time": '2000-01-01T10:10:10.000010',
            "status": 'failure',
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

        assert actual == expected


class TestMergeArgs2Config:
    def test_full_args(self):
        args: Args = Args.from_dict({
            'run': True,
            'files': ['file1', 'file2'],
            'title': 'test_full_args',
            'description': 'Description for test_full_args',
            'config': ['config.yml'],
            'tag': ['tag1', 'tag2'],
            'threads': 3,
            'processes': 2,
            'max_retries': 5,
            'retry': False,
            'init': False,
            'v': 0,
        })

        config: Config = Config.from_dict({
            "title": "Config title",
            "description": "Config description",
            "tags": ["tag3", "tag4"],
            "threads": 1,
            "processes": 4,
            "max_retries": 7,
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy-one",
                "default_response_encoding": "euc-jp",
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other",
                "proxy": "http://proxy-other",
                "default_response_encoding": "euc-jp",
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

        assert merge_args2config(args, config).to_dict() == {
            "title": "test_full_args",
            "description": "Description for test_full_args",
            "tags": ["tag1", "tag2"],
            "threads": 3,
            "processes": 2,
            "max_retries": 5,
            "input_files": ['file1', 'file2'],
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy-one",
                "default_response_encoding": "euc-jp",
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other",
                "proxy": "http://proxy-other",
                "default_response_encoding": "euc-jp",
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "tmpdir"
            },
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

    def test_empty_args(self):
        args: Args = Args.from_dict({
            'run': True,
            'retry': False,
            'init': False,
            'v': 0,
        })

        config: Config = Config.from_dict({
            "title": "Config title",
            "description": "Config description",
            "tags": ["tag3", "tag4"],
            "threads": 1,
            "processes": 4,
            "max_retries": 5,
            "one": {
                "name": "name_one",
                "host": "http://host/one",
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

        assert merge_args2config(args, config).to_dict() == {
            "title": "Config title",
            "description": "Config description",
            "tags": ["tag3", "tag4"],
            "threads": 1,
            "processes": 4,
            "max_retries": 5,
            "one": {
                "name": "name_one",
                "host": "http://host/one",
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
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

    def test_empty_args_and_config(self):
        args: Args = Args.from_dict({
            'run': True,
            'retry': False,
            'init': False,
            'v': 0,
        })

        config: Config = Config.from_dict({
            "one": {
                "name": "name_one",
                "host": "http://host/one",
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

        assert merge_args2config(args, config).to_dict() == {
            "threads": 1,
            "max_retries": 3,
            "one": {
                "name": "name_one",
                "host": "http://host/one",
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
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }


@patch('jumeaux.executor.now')
@patch('jumeaux.executor.challenge')
@patch('jumeaux.executor.hash_from_args')
class TestExec:
    """TODO: Multi process test to fix dead lock!!!
    """

    @classmethod
    def setup_class(cls):
        os.makedirs(os.path.join("tmpdir", "hash_key", "one"))
        os.makedirs(os.path.join("tmpdir", "hash_key", "other"))

    @classmethod
    def teardown_class(cls):
        shutil.rmtree("tmpdir")

    def test(self, hash_from_args, challenge, now):
        dummy_hash = "dummy hash"

        hash_from_args.return_value = dummy_hash
        challenge.side_effect = [
            {
                "seq": 1,
                "name": "name1",
                "request_time": '2000-01-01T10:10:10.000010',
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
                "request_time": '2000-01-01T10:10:11.000010',
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
        ]
        now.side_effect = [
            datetime.datetime(2000, 1, 1, 23, 50, 30, 100),
            datetime.datetime(2000, 1, 2, 0, 0, 0, 200)
        ]

        config: Config = Config.from_dict({
            "title": "Report title",
            "description": "Report description",
            "tags": ["tag1", "tag2"],
            "threads": 1,
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
                },
                "store_criterion": [
                    {
                        "name": "addons.store_criterion.general",
                        "config": {
                            "statuses": [
                                "different"
                            ]
                        }
                    }
                ]
            }
        })
        reqs: TList[Request] = Request.from_dicts([
            {"path": "/dummy"},
            {"path": "/dummy"}
        ])

        actual: Report = executor.exec(config, reqs, dummy_hash, None)

        expected = {
            "version": __version__,
            "key": dummy_hash,
            "title": "Report title",
            "description": "Report description",
            "ignores": [],
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [
                    {
                        "name": "addons.store_criterion.general",
                        "cls_name": "Executor",
                        "config": {
                            "statuses": [
                                "different"
                            ]
                        }
                    }
                ],
                "dump": [],
                "did_challenge": [],
                "final": []
            },
            "summary": {
                "time": {
                    "start": '2000-01-01T23:50:30.000100',
                    "end": '2000-01-02T00:00:00.000200',
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
                "tags": ["tag1", "tag2"],
                "status": {
                    "same": 1,
                    "different": 1,
                    "failure": 0
                },
                "output": {
                    "encoding": "utf8",
                    "response_dir": "tmpdir"
                },
                "concurrency": {
                    "threads": 1,
                    "processes": 1
                }
            },
            "trials": [
                {
                    "seq": 1,
                    "name": "name1",
                    "request_time": '2000-01-01T10:10:10.000010',
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
                    "request_time": '2000-01-01T10:10:11.000010',
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
            ]
        }

        assert actual.to_dict() == expected
