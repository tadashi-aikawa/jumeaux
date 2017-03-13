#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from addons.log.plain_addon import exec


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
        actual = exec('tmp', {"encoding": "utf8"})

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
