#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.log2reqs.csv import Executor
from jumeaux.models import Log2ReqsAddOnPayload

CSV = """
"name1","/path1","q1=1&q2=2","header1=1&header2=2"
"name2","/path2","q1=1&q2=&q3","header1=1&header2=&header3"
"name3","/path3","q1=1"
"name4","/path4",,"header1=1&header2=2"
"name5","/path5"
""".strip()

TSV = """
"name1"	"/path1"	"q1=1&q2=2"	"header1=1&header2=2"
"name2"	"/path2"	"q1=1&q2=&q3"	"header1=1&header2=&header3"
"name3"	"/path3"	"q1=1"
"name4"	"/path4"		"header1=1&header2=2"
"name5"	"/path5"
""".strip()

OVER5 = """
"name","/path","q1=1","header1=1","evil"
""".strip()


def create_expected(no: int, qs: dict, headers: dict) -> dict:
    return {
        "name": f"name{no}",
        "path": f"/path{no}",
        "qs": qs,
        "headers": headers,
    }


class TestExec:
    @pytest.mark.parametrize(
        'title, requests, config_yml, expected', [
            (
                "CSV",
                CSV,
                """
                """,
                [
                    create_expected(1, {"q1": ["1"], "q2": ["2"]}, {"header1": "1", "header2": "2"}),
                    create_expected(2, {"q1": ["1"]}, {"header1": "1"}),
                    create_expected(3, {"q1": ["1"]}, {}),
                    create_expected(4, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, {}, {}),
                ],
            ),
            (
                "TSV",
                TSV,
                """
                dialect: excel-tab
                """,
                [
                    create_expected(1, {"q1": ["1"], "q2": ["2"]}, {"header1": "1", "header2": "2"}),
                    create_expected(2, {"q1": ["1"]}, {"header1": "1"}),
                    create_expected(3, {"q1": ["1"]}, {}),
                    create_expected(4, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, {}, {}),
                ],
            ),
            (
                "CSV with keep_blank true",
                CSV,
                """
                keep_blank: True
                """,
                [
                    create_expected(1, {"q1": ["1"], "q2": ["2"]}, {"header1": "1", "header2": "2"}),
                    create_expected(2,
                                    {"q1": ["1"], "q2": [""], "q3": [""]},
                                    {"header1": "1", "header2": "", "header3": ""}
                                    ),
                    create_expected(3, {"q1": ["1"]}, {}),
                    create_expected(4, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, {}, {}),
                ],
            ),
        ]
    )
    def test(self, create_tmpfile_from, title, requests, config_yml, expected):
        tmp = create_tmpfile_from(requests)
        actual = Executor(load_yaml(config_yml)).exec(Log2ReqsAddOnPayload.from_dict({'file': tmp}))

        assert actual.to_dicts() == expected

    def test_length_over_5(self, create_tmpfile_from):
        tmp = create_tmpfile_from(OVER5)
        with pytest.raises(ValueError):
            Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({'file': tmp}))
