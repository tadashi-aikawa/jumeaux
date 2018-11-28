#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import List

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.did_challenge.tag import Executor
from jumeaux.models import DidChallengeAddOnPayload


def create_trial_dict(seq: int, name: str, tags: List[str], status: str) -> dict:
    return {
        "seq": seq,
        "name": name,
        "tags": tags,
        "headers": {},
        "queries": {},
        "one": {
            "url": "http://one",
            "type": "json",
        },
        "other": {
            "url": "http://other",
            "type": "json",
        },
        "path": "/path",
        "request_time": "2018-11-28T01:29:29.481790+09:00",
        "status": status,
    }


ADD_TAG_IF_CONDITION_IS_FULFILLED = ("Add a tag if a condition is fulfilled",
                                     """
                                     conditions:
                                       - tag: tagged
                                         when: "name == 'hoge'"
                                     """,
                                     create_trial_dict(1, "hoge", [], "same"),
                                     create_trial_dict(1, "hoge", ["tagged"], "same"),
                                     )

ADD_TAGS_IF_CONDITIONS_ARE_FULFILLED = ("Add tags if conditions are fulfilled",
                                        """
                                        conditions:
                                          - tag: tagged1
                                            when: "name == 'hoge'"
                                          - tag: tagged2
                                            when: "name == 'hoge'"
                                        """,
                                        create_trial_dict(1, "hoge", [], "same"),
                                        create_trial_dict(1, "hoge", ["tagged1", "tagged2"], "same"),
                                        )

DO_NOT_ADD_TAG_IF_CONDITION_IS_NOT_FULFILLED = ("Don't Add a tag if a condition is not fulfilled",
                                                """
                                                conditions:
                                                  - tag: tagged
                                                    when: "name == 'hogehoge'"
                                                """,
                                                create_trial_dict(1, "hoge", [], "same"),
                                                create_trial_dict(1, "hoge", [], "same"),
                                                )

ADD_TAG_IF_CONDITION_IS_EMPTY = ("Add a tag if condition is empty",
                                 """
                                 conditions:
                                   - tag: tagged
                                 """,
                                 create_trial_dict(1, "hoge", ["initial"], "same"),
                                 create_trial_dict(1, "hoge", ["initial", "tagged"], "same"),
                                 )

ADD_TAG_FORMATTED = ("Add a tag formatted",
                     """
                     conditions:
                       - tag: "name: {name}"
                     """,
                     create_trial_dict(1, "hoge", [], "same"),
                     create_trial_dict(1, "hoge", ["name: hoge"], "same"),
                     )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, trial, expected_result', [
            ADD_TAG_IF_CONDITION_IS_FULFILLED,
            ADD_TAGS_IF_CONDITIONS_ARE_FULFILLED,
            DO_NOT_ADD_TAG_IF_CONDITION_IS_NOT_FULFILLED,
            ADD_TAG_IF_CONDITION_IS_EMPTY,
            ADD_TAG_FORMATTED,
        ]
    )
    def test(self, title, config_yml, trial, expected_result):
        payload: DidChallengeAddOnPayload = DidChallengeAddOnPayload.from_dict({
            'trial': trial,
        })

        actual: DidChallengeAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert expected_result == actual.trial.to_dict()
