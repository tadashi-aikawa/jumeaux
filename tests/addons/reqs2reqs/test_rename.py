#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.reqs2reqs.rename import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload

RENAME_WITH_CONDITION = ("Rename requests with a condition",
                         """
                         conditions:
                           - name: renamed
                             when: "'target' in path"
                         """,
                         [
                             {"name": "name1", "path": "target", "headers": {}, "qs": {}},
                             {"name": "name2", "path": "TARGET", "headers": {}, "qs": {}},
                             {"name": "name3", "path": "This is target, too", "headers": {}, "qs": {}},
                         ],
                         [
                             {"name": "renamed", "path": "target", "headers": {}, "qs": {}},
                             {"name": "name2", "path": "TARGET", "headers": {}, "qs": {}},
                             {"name": "renamed", "path": "This is target, too", "headers": {}, "qs": {}},
                         ]
                         )

RENAME_WITH_CONDITIONS = ("Rename requests with a conditions",
                          """
                          conditions:
                            - name: Over 100 ({name})
                              when: "qs.id.0|int > 100"
                            - name: Over 10 ({name})
                              when: "qs.id.0|int > 10"
                          """,
                          [
                              {"name": "name1", "path": "target1", "headers": {}, "qs": {'id': ['500']}},
                              {"name": "name2", "path": "target2", "headers": {}, "qs": {'id': ['50']}},
                              {"name": "name3", "path": "target3", "headers": {}, "qs": {'id': ['5']}},
                          ],
                          [
                              {"name": "Over 100 (name1)", "path": "target1", "headers": {}, "qs": {'id': ['500']}},
                              {"name": "Over 10 (name2)", "path": "target2", "headers": {}, "qs": {'id': ['50']}},
                              {"name": "name3", "path": "target3", "headers": {}, "qs": {'id': ['5']}},
                          ]
                          )

RENAME_ALL = ("Rename all",
              """
              conditions:
                - name: target1
                  when: "path == 'target1'"
                - name: END
              """,
              [
                  {"name": "name1", "path": "target1", "headers": {}, "qs": {}},
                  {"name": "name2", "path": "target2", "headers": {}, "qs": {}},
                  {"name": "name3", "path": "target3", "headers": {}, "qs": {}},
              ],
              [
                  {"name": "target1", "path": "target1", "headers": {}, "qs": {}},
                  {"name": "END", "path": "target2", "headers": {}, "qs": {}},
                  {"name": "END", "path": "target3", "headers": {}, "qs": {}},
              ]
              )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, requests, expected_result', [
            RENAME_WITH_CONDITION,
            RENAME_WITH_CONDITIONS,
            RENAME_ALL,
        ]
    )
    def test_rename(self, title, config_yml, requests, expected_result):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': requests,
        })

        actual: Reqs2ReqsAddOnPayload = Executor(load_yaml(config_yml)).exec(payload, None)

        assert expected_result == actual.requests.to_dicts()
