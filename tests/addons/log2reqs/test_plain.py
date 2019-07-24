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
/utf8?word=%e6%9d%b1%e4%ba%ac
/sjis?word=%93%8c%8b%9e
/eucjp?word=%c5%ec%b5%fe
""".strip()


def create_expected(path: str, qs: dict, url_encoding="utf-8") -> dict:
    return {"method": "GET", "path": path, "qs": qs, "headers": {}, "url_encoding": url_encoding}


class TestExec:
    @pytest.mark.parametrize(
        "title, config_yml, expected",
        [
            (
                "Normal",
                """
                """,
                [
                    create_expected("/path1", {"a": ["1"]}),
                    create_expected("/path2", {"a": ["1"], "b": ["2"]}),
                    create_expected("/path3", {"a": ["1", "2"], "b": ["1"]}),
                    create_expected("/path4", {"a": ["1"]}),
                    create_expected("/path5", {"a": ["1"]}),
                    create_expected("/path6", {"a": ["1"], "b": ["あ"]}),
                    create_expected("/path7", {}),
                    create_expected("/path8", {}),
                    create_expected("/utf8", {"word": ["東京"]}),
                    create_expected("/sjis", {"word": ["����"]}),
                    create_expected("/eucjp", {"word": ["���"]}),
                ],
            ),
            (
                "Keep blank",
                """
                keep_blank: True
                """,
                [
                    create_expected("/path1", {"a": ["1"]}),
                    create_expected("/path2", {"a": ["1"], "b": ["2"]}),
                    create_expected("/path3", {"a": ["1", "2"], "b": ["1"]}),
                    create_expected("/path4", {"a": ["1"], "b": [""]}),
                    create_expected("/path5", {"a": ["1"], "b": [""]}),
                    create_expected("/path6", {"a": ["1", ""], "b": ["あ", ""]}),
                    create_expected("/path7", {"a": [""]}),
                    create_expected("/path8", {}),
                    create_expected("/utf8", {"word": ["東京"]}),
                    create_expected("/sjis", {"word": ["����"]}),
                    create_expected("/eucjp", {"word": ["���"]}),
                ],
            ),
            (
                "Specify candidate for url encodings",
                """
                candidate_for_url_encodings:
                  - utf-8
                  - sjis
                """,
                [
                    create_expected("/path1", {"a": ["1"]}),
                    create_expected("/path2", {"a": ["1"], "b": ["2"]}),
                    create_expected("/path3", {"a": ["1", "2"], "b": ["1"]}),
                    create_expected("/path4", {"a": ["1"]}),
                    create_expected("/path5", {"a": ["1"]}),
                    create_expected("/path6", {"a": ["1"], "b": ["あ"]}),
                    create_expected("/path7", {}),
                    create_expected("/path8", {}),
                    create_expected("/utf8", {"word": ["東京"]}),
                    create_expected("/sjis", {"word": ["東京"]}, "sjis"),
                    create_expected("/eucjp", {"word": ["���"]}),
                ],
            ),
        ],
    )
    def test(self, create_tmpfile_from, title, config_yml, expected):
        tmp = create_tmpfile_from(REQUESTS)
        actual = Executor(load_yaml(config_yml)).exec(Log2ReqsAddOnPayload.from_dict({"file": tmp}))

        assert expected == actual.to_dicts()
