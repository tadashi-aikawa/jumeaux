#!/usr/bin/env python
# -*- coding:utf-8 -*-
from unittest.mock import patch, MagicMock

import pytest
from owlmixin import TOption
from owlmixin.util import load_yaml

from jumeaux.addons.reqs2reqs.empty_guard import Executor
from jumeaux.models import Reqs2ReqsAddOnPayload, Notifier
from jumeaux.models import Config as JumeauxConfig

EMPTY = ("Guard empty",
             """
             notifies:
               - notifier: jumeaux
                 message: "{{ title }} notify!"
             """,
             [],
             """
             title: empty test
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
                  channel: "#jumeaux"
                  username: jumeaux
                dummy:
                  type: slack
                  channel: "#dummy"
                  username: dummy
             addons:
                log2reqs:
                  name: plain
             """
             )

NOT_EMPTY = ("Not guard not empty",
         """
         notifies:
           - notifier: jumeaux
             message: "notify!"
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
             {"name": "req", "path": "/sample",  "headers": {}, "qs": {}, 'url_encoding': 'utf-8'}
         ]
         )


def send_for_test(message: str, notifier: Notifier) -> TOption[str]:
    return TOption(message)


@patch('jumeaux.addons.reqs2reqs.empty_guard.send')
class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, requests, jumeaux_config_yml, expected_result', [
            NOT_EMPTY,
        ]
    )
    def test_not_use_notify(self, send, title, config_yml, requests, jumeaux_config_yml, expected_result):
        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': requests,
        })

        actual: Reqs2ReqsAddOnPayload = Executor(load_yaml(config_yml)) \
            .exec(payload, JumeauxConfig.from_yaml(jumeaux_config_yml))

        assert expected_result == actual.requests.to_dicts()

    @pytest.mark.parametrize(
        'title, config_yml, requests, jumeaux_config_yml', [
            EMPTY,
        ]
    )
    def test_use_notify(self, send, title, config_yml, requests, jumeaux_config_yml):
        send.side_effect = send_for_test

        payload: Reqs2ReqsAddOnPayload = Reqs2ReqsAddOnPayload.from_dict({
            'requests': requests,
        })

        try:
            Executor(load_yaml(config_yml)) \
                .exec(payload, JumeauxConfig.from_yaml(jumeaux_config_yml))
        except SystemExit:
            assert send.call_args[0][0] == 'empty test notify!'
            assert send.call_args[0][1].to_dict() == {
                "type": "slack",
                "channel": "#jumeaux",
                "username": "jumeaux"
            }
