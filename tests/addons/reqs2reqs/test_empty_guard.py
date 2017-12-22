#!/usr/bin/env python
# -*- coding:utf-8 -*-
from unittest.mock import patch

import pytest
from owlmixin import TOption
from owlmixin.util import load_yaml

from jumeaux.addons.reqs2reqs.empty_guard import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload
from jumeaux.models import Config as JumeauxConfig

EMPTY = ("Guard empty",
             """
             notifies:
               - notifier: jumeaux
                 message: notify!
             """,
             [],
             """
             one:
                name: one
                host: http://one   
             other:
                name: other
                host: http://other
             output:
                response_dir: responses
             notifiers:
                jumeaux:
                type: slack
                channel: "#hogehoge"
                username: hogehoge
             addons:
                log2reqs:
                  name: plain
             """,
             []
             )

NOT_EMPTY = ("Not guard not empty",
         """
         notifies:
           - notifier: jumeaux
             message: notify!
         """,
         [
             {"name": "req", "path": "/sample", "headers": {}, "qs": {}}
         ],
         """
         one:
            name: one
            host: http://one   
         other:
            name: other
            host: http://other
         output:
            response_dir: responses
         addons:
            log2reqs:
              name: plain
         """,
         [
             {"name": "req", "path": "/sample",  "headers": {}, "qs": {}}
         ]
         )


@patch('jumeaux.addons.reqs2reqs.empty_guard.send')
class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, requests, jumeaux_config_yml, expected_result', [
            EMPTY,
            NOT_EMPTY,
        ]
    )
    def test(self, send, title, config_yml, requests, jumeaux_config_yml, expected_result):
        send.side_effect = TOption(None)

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': requests,
        })

        actual: Reqs2ReqsAddOnPayload = Executor(load_yaml(config_yml)) \
            .exec(payload, JumeauxConfig.from_yaml(jumeaux_config_yml))

        assert actual.requests.to_dicts() == expected_result
