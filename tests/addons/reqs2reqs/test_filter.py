#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.reqs2reqs.filter import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload

AND = ("And filter",
       """
       and_or: and
       filters:
         - path:
             items:
               - regexp: .*ok.*
         - name:
             items:
               - regexp: .*OK.*
       """,
       [
           {"name": "It's OK", "path": "/ok", "headers": {}, "qs": {}},
           {"name": "It's OK", "path": "/ng", "headers": {}, "qs": {}},
           {"name": "It's NG", "path": "/ok", "headers": {}, "qs": {}},
           {"name": "It's NG", "path": "/ng", "headers": {}, "qs": {}},
       ],
       [
           {"name": "It's OK", "path": "/ok", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
       ]
       )

OR = ("Or filter",
      """
      and_or: or
      filters:
        - path:
            items:
              - regexp: .*ok.*
        - name:
            items:
              - regexp: .*OK.*
      """,
      [
          {"name": "It's OK", "path": "/ok", "headers": {}, "qs": {}},
          {"name": "It's OK", "path": "/ng", "headers": {}, "qs": {}},
          {"name": "It's NG", "path": "/ok", "headers": {}, "qs": {}},
          {"name": "It's NG", "path": "/ng", "headers": {}, "qs": {}},
      ],
      [
          {"name": "It's OK", "path": "/ok", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
          {"name": "It's OK", "path": "/ng", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
          {"name": "It's NG", "path": "/ok", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
      ]
      )

NEGATIVE = ("Negative filter",
            """
            negative: true
            filters:
              - path:
                  items:
                    - regexp: .*ok.*
              - name:
                  items:
                    - regexp: .*OK.*
            """,
            [
                {"name": "It's OK", "path": "/ok", "headers": {}, "qs": {}},
                {"name": "It's OK", "path": "/ng", "headers": {}, "qs": {}},
                {"name": "It's NG", "path": "/ok", "headers": {}, "qs": {}},
                {"name": "It's NG", "path": "/ng", "headers": {}, "qs": {}},
            ],
            [
                {"name": "It's OK", "path": "/ng", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
                {"name": "It's NG", "path": "/ok", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
                {"name": "It's NG", "path": "/ng", "headers": {}, "qs": {}, 'url_encoding': 'utf-8'},
            ]
            )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, requests, expected_result', [
            AND,
            OR,
            NEGATIVE
        ]
    )
    def test_filter(self, title, config_yml, requests, expected_result):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': requests,
        })

        actual: Reqs2ReqsAddOnPayload = Executor(load_yaml(config_yml)).exec(payload, None)

        assert expected_result == actual.requests.to_dicts()
