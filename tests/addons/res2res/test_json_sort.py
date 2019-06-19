#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2res.json_sort import Executor
from jumeaux.models import Res2ResAddOnPayload, Response

TEXT = json.dumps({
    "int1": 1,
    "str1": "1",
    "dict1": {
        "list1-1": ["o", "w", "l"]
    },
    "list1": ["o", "w", "l"],
    "list2": [
        {"id": 2, "name": "ccc"},
        {"id": 1, "name": "bbb"},
        {"id": 2, "name": "aaa"}
    ],
    "list3": [
        {"list3-1": ["o", "w", "l"]},
        {"list3-2": ["o", "w", "l"]}
    ],
    "list4": [
        {
            "list4-2": [
                {"id": 1, "names": ["o", "w", "l"]}
            ]
        },
        {
            "list4-1": [
                {"id": 2, "names": ["o", "w", "l"]},
                {"id": 1, "names": ["o", "w", "l"]}
            ]
        }
    ],
    "list5": ["l", "o", "w"],
})


TEXT_MULTIBYTE = json.dumps({
    "name": "国道１２３号"
})


def make_response(text: str, encoding: str, body_encoding: str) -> Response:
    return Response.from_dict({
        "body": text.encode(body_encoding),
        "type": "json",
        "encoding": encoding,
        "headers": {
            "content-type": "application/json"
        },
        "url": "http://test",
        "status_code": 200,
        "elapsed": datetime.timedelta(seconds=1),
        "elapsed_sec": 1.0,
    })


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, expected_tags, expected_text', [
            (
                "dict -> list(str) (string sorting)",
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'dict1'><'list1-1'>
                """,
                ["default"],
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["l", "o", "w"]
                    },
                    "list1": ["o", "w", "l"],
                    "list2": [
                        {"id": 2, "name": "ccc"},
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["o", "w", "l"]}
                    ],
                    "list4": [
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            ),
            (
                "list(str) (string sorting)",
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'list1'>
                """,
                ["default"],
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["o", "w", "l"]
                    },
                    "list1": ["l", "o", "w"],
                    "list2": [
                        {"id": 2, "name": "ccc"},
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["o", "w", "l"]}
                    ],
                    "list4": [
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            ),
            (
                "list(dict) (dict sorting with specified keys)",
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'list2'>
                        sort_keys: [id, name]
                """,
                ["default"],
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["o", "w", "l"]
                    },
                    "list1": ["o", "w", "l"],
                    "list2": [
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"},
                        {"id": 2, "name": "ccc"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["o", "w", "l"]}
                    ],
                    "list4": [
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            ),
            (
                "list -> dict -> list(str) (string sorting)",
                r"""
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'list3'><\d+><'list3-2'>
                footprints_tag: "changed"
                """,
                ["default", "changed"],
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["o", "w", "l"]
                    },
                    "list1": ["o", "w", "l"],
                    "list2": [
                        {"id": 2, "name": "ccc"},
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["l", "o", "w"]}
                    ],
                    "list4": [
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            ),
            (
                "list -> * (dict sorting without keys)",
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'list4'>
                footprints_tag: "changed"
                """,
                ["default", "changed"],
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["o", "w", "l"]
                    },
                    "list1": ["o", "w", "l"],
                    "list2": [
                        {"id": 2, "name": "ccc"},
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["o", "w", "l"]}
                    ],
                    "list4": [
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            )
        ]
    )

    def test_normal(self, title, config_yml, expected_tags, expected_text):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response(TEXT, 'utf-8', 'utf-8'),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": ["default"],
        })

        expected = {
            'response': make_response(json.dumps(expected_text), 'utf-8', 'utf-8').to_dict(),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": expected_tags,
        }
        actual = Executor(load_yaml(config_yml)).exec(payload).to_dict()

        assert expected == actual

    @pytest.mark.parametrize(
        'title, config_yml, expected_text', [
            (
                "dict -> list(str) (string sorting)",
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'list5'>
                footprints_tag: "changed"
                """,
                {
                    "int1": 1,
                    "str1": "1",
                    "dict1": {
                        "list1-1": ["o", "w", "l"],
                    },
                    "list1": ["o", "w", "l"],
                    "list2": [
                        {"id": 2, "name": "ccc"},
                        {"id": 1, "name": "bbb"},
                        {"id": 2, "name": "aaa"}
                    ],
                    "list3": [
                        {"list3-1": ["o", "w", "l"]},
                        {"list3-2": ["o", "w", "l"]}
                    ],
                    "list4": [
                        {
                            "list4-2": [
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        },
                        {
                            "list4-1": [
                                {"id": 2, "names": ["o", "w", "l"]},
                                {"id": 1, "names": ["o", "w", "l"]}
                            ]
                        }
                    ],
                    "list5": ["l", "o", "w"],
                }
            ),
        ]
    )
    def test_sorted_bat_same(self, title, config_yml, expected_text):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response(TEXT, 'utf-8', 'utf-8'),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": ["default"],
        })

        expected = {
            'response': make_response(json.dumps(expected_text), 'utf-8', 'utf-8').to_dict(),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": ["default"],
        }
        actual = Executor(load_yaml(config_yml)).exec(payload).to_dict()

        assert expected == actual
    @pytest.mark.parametrize(
        'title, encoding, body_encoding, config_yml, expected_text', [
            (
                "Valid encoding",
                'utf-8',
                'utf-8',
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'name'>
                footprints_tag: "changed"
                """,
                {
                    "name": "国道１２３号",
                }
            ),
            (
                "Illegal encoding",
                'Windows-1254',
                'sjis',
                """
                items:
                  - conditions:
                      - path:
                          items:
                            - regexp: /filter
                    targets:
                      - path: root<'name'>
                """,
                {
                    "name": "??????",
                }
            )
        ]
    )
    def test_multibyte(self, title, encoding, body_encoding, config_yml, expected_text):
        payload: Res2ResAddOnPayload = Res2ResAddOnPayload.from_dict({
            'response': make_response(TEXT_MULTIBYTE, encoding, body_encoding),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": ["default"],
        })

        actual = Executor(load_yaml(config_yml)).exec(payload).to_dict()
        expected = {
            'response': make_response(json.dumps(expected_text, ensure_ascii=False), encoding, encoding).to_dict(),
            'req': {
                "path": "/filter",
                "qs": {},
                "headers": {},
                "url_encoding": "utf-8",
            },
            "tags": ["default"],
        }


        assert expected == actual

