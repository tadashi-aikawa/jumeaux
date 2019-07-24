#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.log2reqs.csv import Executor
from jumeaux.models import Log2ReqsAddOnPayload, HttpMethod

CSV = """
"name1","GET","/path1","q1=1&q2=2","header1=1&header2=2"
"name2","POST","/path2","q1=1&q2=&q3","header1=1&header2=&header3"
"name3","GET","/path3","q1=1"
"name4","POST","/path4",,"header1=1&header2=2"
"name5","GET","/path5"
""".strip()

TSV = """
"name1"	"GET"	"/path1"	"q1=1&q2=2"	"header1=1&header2=2"
"name2"	"POST"	"/path2"	"q1=1&q2=&q3"	"header1=1&header2=&header3"
"name3"	"GET"	"/path3"	"q1=1"
"name4"	"POST"	"/path4"		"header1=1&header2=2"
"name5"	"GET"	"/path5"
""".strip()

OVER5 = """
"name","GET","/path","q1=1","header1=1","evil"
""".strip()


def create_expected(no: int, method: HttpMethod, qs: dict, headers: dict) -> dict:
    return {
        "name": f"name{no}",
        "method": method.to_value(True, True),
        "path": f"/path{no}",
        "qs": qs,
        "headers": headers,
        "url_encoding": "utf-8",
    }


class TestExec:
    @pytest.mark.parametrize(
        "title, requests, config_yml, expected",
        [
            (
                "CSV",
                CSV,
                """
                """,
                [
                    create_expected(
                        1,
                        HttpMethod.GET,
                        {"q1": ["1"], "q2": ["2"]},
                        {"header1": "1", "header2": "2"},
                    ),
                    create_expected(2, HttpMethod.POST, {"q1": ["1"]}, {"header1": "1"}),
                    create_expected(3, HttpMethod.GET, {"q1": ["1"]}, {}),
                    create_expected(4, HttpMethod.POST, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, HttpMethod.GET, {}, {}),
                ],
            ),
            (
                "TSV",
                TSV,
                """
                dialect: excel-tab
                """,
                [
                    create_expected(
                        1,
                        HttpMethod.GET,
                        {"q1": ["1"], "q2": ["2"]},
                        {"header1": "1", "header2": "2"},
                    ),
                    create_expected(2, HttpMethod.POST, {"q1": ["1"]}, {"header1": "1"}),
                    create_expected(3, HttpMethod.GET, {"q1": ["1"]}, {}),
                    create_expected(4, HttpMethod.POST, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, HttpMethod.GET, {}, {}),
                ],
            ),
            (
                "CSV with keep_blank true",
                CSV,
                """
                keep_blank: True
                """,
                [
                    create_expected(
                        1,
                        HttpMethod.GET,
                        {"q1": ["1"], "q2": ["2"]},
                        {"header1": "1", "header2": "2"},
                    ),
                    create_expected(
                        2,
                        HttpMethod.POST,
                        {"q1": ["1"], "q2": [""], "q3": [""]},
                        {"header1": "1", "header2": "", "header3": ""},
                    ),
                    create_expected(3, HttpMethod.GET, {"q1": ["1"]}, {}),
                    create_expected(4, HttpMethod.POST, {}, {"header1": "1", "header2": "2"}),
                    create_expected(5, HttpMethod.GET, {}, {}),
                ],
            ),
        ],
    )
    def test(self, create_tmpfile_from, title, requests, config_yml, expected):
        tmp = create_tmpfile_from(requests)
        actual = Executor(load_yaml(config_yml)).exec(Log2ReqsAddOnPayload.from_dict({"file": tmp}))

        assert actual.to_dicts() == expected

    def test_length_over_5(self, create_tmpfile_from):
        tmp = create_tmpfile_from(OVER5)
        with pytest.raises(ValueError):
            Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({"file": tmp}))
