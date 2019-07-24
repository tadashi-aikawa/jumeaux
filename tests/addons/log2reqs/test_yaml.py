#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest
from owlmixin import RequiredError

from jumeaux.addons.log2reqs.yaml import Executor
from jumeaux.models import Log2ReqsAddOnPayload


class TestFromFormat:
    @classmethod
    def teardown_class(cls):
        os.path.exists("tmp") and os.remove("tmp")

    def test_yaml(self):
        examinee = """
- path: "/test1"
- path: "/test2"
  method: "GET"
  qs:
    q1:
      - "1"
- path: "/test3"
  method: "POST"
  form:
    form_key: [1, 2]
  qs:
    q1:
      - "1"
    q2:
      - "2-1"
      - "2-2"
- path: "/test4"
  method: "POST"
  json: {"root": {"id": 100}}
  headers:
    key1: "header1"
    key2: "header2"
- path: "/test5"
  qs:
    q1:
      - "1"
    q2:
      - "2-1"
      - "2-2"
  headers:
    key1: "header1"
    key2: "header2"
""".strip()
        with open("tmp", "w", encoding="utf8") as f:
            f.write(examinee)
        actual = Executor({"encoding": "utf8"}).exec(
            Log2ReqsAddOnPayload.from_dict({"file": "tmp"})
        )

        expected = [
            {"method": "GET", "path": "/test1", "qs": {}, "headers": {}, "url_encoding": "utf-8"},
            {
                "method": "GET",
                "path": "/test2",
                "qs": {"q1": ["1"]},
                "headers": {},
                "url_encoding": "utf-8",
            },
            {
                "method": "POST",
                "path": "/test3",
                "form": {"form_key": [1, 2]},
                "qs": {"q1": ["1"], "q2": ["2-1", "2-2"]},
                "headers": {},
                "url_encoding": "utf-8",
            },
            {
                "method": "POST",
                "path": "/test4",
                "json": {"root": {"id": 100}},
                "qs": {},
                "headers": {"key1": "header1", "key2": "header2"},
                "url_encoding": "utf-8",
            },
            {
                "method": "GET",
                "path": "/test5",
                "qs": {"q1": ["1"], "q2": ["2-1", "2-2"]},
                "headers": {"key1": "header1", "key2": "header2"},
                "url_encoding": "utf-8",
            },
        ]

        assert actual.to_dicts() == expected

    def test_yaml_path_not_exist(self):
        examinee = """
- qs: ""
""".strip()

        with open("tmp", "w", encoding="utf8") as f:
            f.write(examinee)
        with pytest.raises(RequiredError):
            Executor({"encoding": "utf8"}).exec(Log2ReqsAddOnPayload.from_dict({"file": "tmp"}))
