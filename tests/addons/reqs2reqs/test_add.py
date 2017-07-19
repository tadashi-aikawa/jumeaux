#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jumeaux.addons.reqs2reqs.add import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload


class TestExec:

    def test(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': [
                {'path': '/origin', 'headers': {'h1': 'header1'}, 'qs': {'q1': ['query1']}}
            ]
        })

        actual: Reqs2ReqsAddOnPayload = Executor({
            'reqs': [
                {'path': '/added1', 'qs': {'q2': ['query2']}},
                {'path': '/added2', 'headers': {'h2': 'header2'}},
            ]
        }).exec(payload)

        assert actual.to_dict() == {
            'requests': [
                {'path': '/added1', 'headers': {}, 'qs': {'q2': ['query2']}},
                {'path': '/added2', 'headers': {'h2': 'header2'}, 'qs': {}},
                {'path': '/origin', 'headers': {'h1': 'header1'}, 'qs': {'q1': ['query1']}},
            ]
        }

    def test_head(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': [
                {'path': '/origin', 'headers': {}, 'qs': {}}
            ]
        })

        actual: Reqs2ReqsAddOnPayload = Executor({
            'reqs': [
                {'path': '/added'}
            ]
        }).exec(payload)

        assert actual.to_dict() == {
            'requests': [
                {'path': '/added', 'headers': {}, 'qs': {}},
                {'path': '/origin', 'headers': {}, 'qs': {}},
            ]
        }

    def test_tail(self):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': [
                {'path': '/origin', 'headers': {}, 'qs': {}}
            ]
        })

        actual: Reqs2ReqsAddOnPayload = Executor({
            'location': 'tail',
            'reqs': [
                {'path': '/added'}
            ]
        }).exec(payload)

        assert actual.to_dict() == {
            'requests': [
                {'path': '/origin', 'headers': {}, 'qs': {}},
                {'path': '/added', 'headers': {}, 'qs': {}},
            ]
        }
