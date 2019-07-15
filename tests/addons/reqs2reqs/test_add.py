#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jumeaux.addons.reqs2reqs.add import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload


class TestExec:
    def test(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict(
            {
                "requests": [
                    {"path": "/origin", "headers": {"h1": "header1"}, "qs": {"q1": ["query1"]}}
                ]
            }
        )

        actual: Reqs2ReqsAddOnPayload = Executor(
            {
                "reqs": [
                    {"path": "/added1", "qs": {"q2": ["query2"]}},
                    {"path": "/added2", "headers": {"h2": "header2"}},
                ]
            }
        ).exec(payload, None)

        assert actual.to_dict() == {
            "requests": [
                {
                    "method": "GET",
                    "path": "/added1",
                    "headers": {},
                    "qs": {"q2": ["query2"]},
                    "url_encoding": "utf-8",
                },
                {
                    "method": "GET",
                    "path": "/added2",
                    "headers": {"h2": "header2"},
                    "qs": {},
                    "url_encoding": "utf-8",
                },
                {
                    "method": "GET",
                    "path": "/origin",
                    "headers": {"h1": "header1"},
                    "qs": {"q1": ["query1"]},
                    "url_encoding": "utf-8",
                },
            ]
        }

    def test_head(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict(
            {"requests": [{"path": "/origin", "headers": {}, "qs": {}}]}
        )

        actual: Reqs2ReqsAddOnPayload = Executor({"reqs": [{"path": "/added"}]}).exec(payload, None)

        assert actual.to_dict() == {
            "requests": [
                {
                    "method": "GET",
                    "path": "/added",
                    "headers": {},
                    "qs": {},
                    "url_encoding": "utf-8",
                },
                {
                    "method": "GET",
                    "path": "/origin",
                    "headers": {},
                    "qs": {},
                    "url_encoding": "utf-8",
                },
            ]
        }

    def test_tail(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict(
            {"requests": [{"path": "/origin", "headers": {}, "qs": {}}]}
        )

        actual: Reqs2ReqsAddOnPayload = Executor(
            {"location": "tail", "reqs": [{"path": "/added"}]}
        ).exec(payload, None)

        assert actual.to_dict() == {
            "requests": [
                {
                    "method": "GET",
                    "path": "/origin",
                    "headers": {},
                    "qs": {},
                    "url_encoding": "utf-8",
                },
                {
                    "method": "GET",
                    "path": "/added",
                    "headers": {},
                    "qs": {},
                    "url_encoding": "utf-8",
                },
            ]
        }
