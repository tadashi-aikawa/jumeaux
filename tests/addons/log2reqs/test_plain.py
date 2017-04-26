#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from jumeaux.addons.log2reqs.plain import Executor
from jumeaux.models import Log2ReqsAddOnPayload


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
        actual = Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': 'tmp'}))

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
