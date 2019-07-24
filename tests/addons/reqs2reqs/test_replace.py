#!/usr/bin/env python
# -*- coding:utf-8 -*-
import freezegun
import pytest

from jumeaux.addons.reqs2reqs.replace import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload
from owlmixin.util import load_yaml


class TestRequestCondition:
    @pytest.mark.parametrize(
        "reqs, expected",
        [
            (
                [
                    {
                        "name": "hoge",
                        "method": "GET",
                        "path": "/api",
                        "qs": {"q1": ["v11"], "q2": ["v21", "v22"]},
                        "headers": {},
                    }
                ],
                [
                    {
                        "name": "hoge",
                        "method": "GET",
                        "path": "/api",
                        "qs": {"q1": ["v99"], "q2": ["v999"]},
                        "headers": {},
                        "url_encoding": "utf-8",
                    }
                ],
            ),
            (
                [
                    {
                        "name": "hoge",
                        "method": "GET",
                        "path": "/hogehoge",
                        "qs": {"q1": ["v11"], "q2": ["v21", "v22"]},
                        "headers": {"h2": "header2", "h3": "header3"},
                    }
                ],
                [
                    {
                        "name": "hoge",
                        "method": "GET",
                        "path": "/hogehoge",
                        "qs": {"q1": ["v77"], "q2": ["v21", "v22"], "q3": ["v777"]},
                        "headers": {"h1": "H1", "h2": "H2", "h3": "header3"},
                        "url_encoding": "utf-8",
                    }
                ],
            ),
        ],
    )
    def test_static(self, reqs, expected):
        config = load_yaml(
            """
items:
  - when: path == '/api' and name == 'hoge'
    queries:
      q1: ['v99']
      q2: ['v999']
  - when: path == '/hogehoge'
    queries:
      q1: ['v77']
      q3: ['v777']
    headers:
      h1: H1
      h2: H2
        """
        )

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({"requests": reqs})

        assert Executor(config).exec(payload, None).to_dict() == {"requests": expected}

    @pytest.mark.parametrize(
        "q1, reqs, expected",
        [
            (
                ["$DATETIME(%Y-%m-%dT%H:%M:%S)(3600)"],
                [{"method": "GET", "path": "/api", "qs": {"q1": ["v99"]}, "headers": {}}],
                [
                    {
                        "method": "GET",
                        "path": "/api",
                        "qs": {"q1": ["2000-01-01T10:00:00"]},
                        "headers": {},
                        "url_encoding": "utf-8",
                    }
                ],
            ),
            (
                ["$DATETIME(%Y/%m/%d %H:%M:%S)(-666)"],
                [{"method": "GET", "path": "/api", "qs": {"q1": ["v99"]}, "headers": {}}],
                [
                    {
                        "method": "GET",
                        "path": "/api",
                        "qs": {"q1": ["2000/01/01 08:48:54"]},
                        "headers": {},
                        "url_encoding": "utf-8",
                    }
                ],
            ),
        ],
    )
    @freezegun.freeze_time("2000-01-01 09:00:00")
    def test_datetime(self, q1, reqs, expected):
        config = {"items": [{"queries": {"q1": q1}}]}

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({"requests": reqs})

        assert Executor(config).exec(payload, None).to_dict() == {"requests": expected}
