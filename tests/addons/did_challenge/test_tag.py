#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import List
import datetime

import pytest
from owlmixin.util import load_yaml

from jumeaux.addons.did_challenge.tag import Executor
from jumeaux.models import DidChallengeAddOnPayload, DidChallengeAddOnReference, Response, CaseInsensitiveDict


RES_ONE = Response.from_dict({
    'body': b'a',
    "type": "unknown",
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=1),
    "elapsed_sec": 1.0,
})


RES_OTHER = Response.from_dict({
    'body': b'b',
    "type": "unknown",
    'headers': CaseInsensitiveDict({}),
    'url': 'url',
    'status_code': 200,
    'elapsed': datetime.timedelta(seconds=2),
    "elapsed_sec": 2.0,
})


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
                                         when: "trial.name == 'hoge'"
                                     """,
                                     create_trial_dict(1, "hoge", [], "same"),
                                     create_trial_dict(1, "hoge", ["tagged"], "same"),
                                     )

ADD_TAGS_IF_CONDITIONS_ARE_FULFILLED = ("Add tags if conditions are fulfilled",
                                        """
                                        conditions:
                                          - tag: tagged1
                                            when: "trial.name == 'hoge'"
                                          - tag: tagged2
                                            when: "trial.name == 'hoge'"
                                        """,
                                        create_trial_dict(1, "hoge", [], "same"),
                                        create_trial_dict(1, "hoge", ["tagged1", "tagged2"], "same"),
                                        )

DO_NOT_ADD_TAG_IF_CONDITION_IS_NOT_FULFILLED = ("Don't Add a tag if a condition is not fulfilled",
                                                """
                                                conditions:
                                                  - tag: tagged
                                                    when: "trial.name == 'hogehoge'"
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
                       - tag: "{trial[name]}: {res_one[elapsed_sec]}"
                     """,
                     create_trial_dict(1, "hoge", [], "same"),
                     create_trial_dict(1, "hoge", ["hoge: 1.0"], "same"),
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
        reference: DidChallengeAddOnReference = DidChallengeAddOnReference.from_dict({
            "res_one": RES_ONE,
            "res_other": RES_OTHER
        })

        actual: DidChallengeAddOnPayload = Executor(load_yaml(config_yml)).exec(payload, reference)

        assert expected_result == actual.trial.to_dict()
