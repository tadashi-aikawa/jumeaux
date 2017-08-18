#!/usr/bin/env python
# -*- coding:utf-8 -*-
import freezegun
import pytest

from jumeaux.addons.reqs2reqs.replace_queries import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload
from owlmixin.util import load_yaml


class TestRequestCondition:
    @pytest.mark.parametrize(
        'reqs, expected', [
            (
                [{'name': 'hoge', 'path': '/api', 'qs': {'q1': ['v11'], 'q2': ['v21', 'v22']}, 'headers': {}}],
                [{'name': 'hoge', 'path': '/api', 'qs': {'q1': ['v99'], 'q2': ['v999']}, 'headers': {}}],
            ),
            (
                [{'name': 'hoge', 'path': '/hogehoge', 'qs': {'q1': ['v11'], 'q2': ['v21', 'v22']}, 'headers': {}}],
                [{'name': 'hoge', 'path': '/hogehoge', 'qs': {'q1': ['v77'], 'q2': ['v21', 'v22'], 'q3': ['v777']},
                  'headers': {}}],
            ),
        ]
    )
    def test_static(self, reqs, expected):
        config = load_yaml("""
items:
  - conditions:
      - path:
          items:
            - regexp: /api
      - name:
          items:
            - regexp: hoge
    queries:
      q1: ['v99']
      q2: ['v999']
  - conditions:
      - path:
          items:
            - regexp: /hogehoge
    queries:
      q1: ['v77']
      q3: ['v777']
        """)

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': reqs
        })

        assert Executor(config).exec(payload).to_dict() == {
            'requests': expected
        }

    @pytest.mark.parametrize(
        'q1, reqs, expected', [
            (
                ['$DATETIME(%Y-%m-%dT%H:%M:%S)(3600)'],
                [{'path': '/api', 'qs': {'q1': ['v99']}, 'headers': {}}],
                [{'path': '/api', 'qs': {'q1': ['2000-01-01T10:00:00']}, 'headers': {}}],
            ),
            (
                ['$DATETIME(%Y/%m/%d %H:%M:%S)(-666)'],
                [{'path': '/api', 'qs': {'q1': ['v99']}, 'headers': {}}],
                [{'path': '/api', 'qs': {'q1': ['2000/01/01 08:48:54']}, 'headers': {}}],
            ),
        ]
    )
    @freezegun.freeze_time('2000-01-01 09:00:00')
    def test_datetime(self, q1, reqs, expected):
        config = {
            'items': [
                {
                    'conditions': [],
                    'queries': {
                        'q1': q1
                    }
                }
            ]
        }

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': reqs
        })

        assert Executor(config).exec(payload).to_dict() == {
            'requests': expected
        }
