#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.log2reqs.plain import Executor
from jumeaux.models import Log2ReqsAddOnPayload

# Line break is ignored. (examinee has 3 not 4)
REQUESTS = """
/path1?a=1
/path2?a=1&b=2
/path3?a=1&a=2&b=1
/path4?a=1&b
/path5?a=1&b=
/path6?a=1&a&b=あ&b=
/path7?a

/path8
""".strip()


def create_expected(no: int, qs: dict) -> dict:
    return {
        "path": f"/path{no}",
        "qs": qs,
        "headers": {}
    }


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, expected', [
            (
                "Normal",
                """
                """,
                [
                    create_expected(1, {"a": ["1"]}),
                    create_expected(2, {"a": ["1"], "b": ["2"]}),
                    create_expected(3, {"a": ["1", "2"], "b": ["1"]}),
                    create_expected(4, {"a": ["1"]}),
                    create_expected(5, {"a": ["1"]}),
                    create_expected(6, {"a": ["1"], "b": ["あ"]}),
                    create_expected(7, {}),
                    create_expected(8, {}),
                ]
            ),
            (
                "Keep blank",
                """
                keep_blank: True
                """,
                [
                    create_expected(1, {"a": ["1"]}),
                    create_expected(2, {"a": ["1"], "b": ["2"]}),
                    create_expected(3, {"a": ["1", "2"], "b": ["1"]}),
                    create_expected(4, {"a": ["1"], "b": [""]}),
                    create_expected(5, {"a": ["1"], "b": [""]}),
                    create_expected(6, {"a": ["1", ""], "b": ["あ", ""]}),
                    create_expected(7, {"a": [""]}),
                    create_expected(8, {}),
                ]
            ),
        ]
    )
    def test(self, create_tmpfile_from, title, config_yml, expected):
        tmp = create_tmpfile_from(REQUESTS)
        actual = Executor(load_yaml(config_yml)).exec(Log2ReqsAddOnPayload.from_dict({'file': tmp}))

        assert expected == actual.to_dicts()
