#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2dict.block import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

PATTERN1_BODY = """
[Module1]
Name: Jumeaux
License: MIT
Version: 0.33.0

[Module2 alpha]
Name: Jumeaux Viewer
Version: 1.0.0 (r: 1585:1586)
""".lstrip()

PATTERN2_BODY = """
1)Module1
Name Jumeaux
License MIT
Version 0.33.0

2)Module2 alpha
Name Jumeaux Viewer
Version 1.0.0 (r1585)
""".lstrip()

NO_END_LINEBREAK_BODY = """
[Module1]
Name: Jumeaux
License: MIT
Version: 0.33.0

[Module2 alpha]
Name: Jumeaux Viewer
Version: 1.0.0 (r1585)
""".strip()

PATTERN1 = ("Normal",
            """
            force: False 
            header_regexp: '\\[(.+)\\]'
            record_regexp: '([^:]+): (.+)'
            """,
            Response.from_dict({
                "body": PATTERN1_BODY.encode('utf-8'),
                "type": "plain",
                "encoding": 'utf-8',
                "headers": {
                    "content-type": "text/plain; charset=utf-8"
                },
                "url": "http://test",
                "status_code": 200,
                "elapsed": datetime.timedelta(seconds=1),
                "elapsed_sec": 1.0,
            }),
            {
                "Module1": {
                    "Name": "Jumeaux",
                    "License": "MIT",
                    "Version": "0.33.0"
                },
                "Module2 alpha": {
                    "Name": "Jumeaux Viewer",
                    "Version": "1.0.0 (r: 1585:1586)"
                }
            }
            )

PATTERN2 = ("Normal",
            """
            force: False 
            header_regexp: '^\\d+\\)(.+)'
            record_regexp: '([^ ]+) (.+)'
            """,
            Response.from_dict({
                "body": PATTERN2_BODY.encode('utf-8'),
                "type": "plain",
                "encoding": 'utf-8',
                "headers": {
                    "content-type": "text/plain; charset=utf-8"
                },
                "url": "http://test",
                "status_code": 200,
                "elapsed": datetime.timedelta(seconds=1),
                "elapsed_sec": 1.0,
            }),
            {
                "Module1": {
                    "Name": "Jumeaux",
                    "License": "MIT",
                    "Version": "0.33.0"
                },
                "Module2 alpha": {
                    "Name": "Jumeaux Viewer",
                    "Version": "1.0.0 (r1585)"
                }
            }
            )

NO_END_LINEBREAK = ("No end linebreak",
                    """
                    force: False 
                    header_regexp: '\\[(.+)\\]'
                    record_regexp: '([^:]+): (.+)'
                    """,
                    Response.from_dict({
                        "body": NO_END_LINEBREAK_BODY.encode('utf-8'),
                        "type": "plain",
                        "encoding": 'utf-8',
                        "headers": {
                            "content-type": "text/plain; charset=utf-8"
                        },
                        "url": "http://test",
                        "status_code": 200,
                        "elapsed": datetime.timedelta(seconds=1),
                        "elapsed_sec": 1.0,
                    }),
                    {
                        "Module1": {
                            "Name": "Jumeaux",
                            "License": "MIT",
                            "Version": "0.33.0"
                        },
                        "Module2 alpha": {
                            "Name": "Jumeaux Viewer",
                            "Version": "1.0.0 (r1585)"
                        }
                    }
                    )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, expected_result', [
            PATTERN1,
            PATTERN2,
            NO_END_LINEBREAK,
        ]
    )
    def test(self, title, config_yml, response, expected_result):
        payload: Res2DictAddOnPayload = Res2DictAddOnPayload.from_dict({
            'response': response,
        })

        actual: Res2DictAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert actual.response == response
        assert actual.result.get() == expected_result
