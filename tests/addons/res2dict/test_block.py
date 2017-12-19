#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2dict.block import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

NORMAL_BODY = """
[Module1]
Name: Jumeaux
License: MIT
Version: 0.33.0

[Module2 alpha]
Name: Jumeaux Viewer
Version: 1.0.0 (r: 1585:1586)
""".lstrip()

CUSTOM_PATTERN_BODY = """
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

NORMAL_CASE = ("Normal",
               """
               force: False 
               mime_types:
                 - text/plain
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('utf-8'),
                   "encoding": 'utf-8',
                   "text": NORMAL_BODY,
                   "headers": {
                       "content-type": "text/plain; charset=utf-8"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
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

CUSTOM_PATTERN = ("Normal",
               """
               force: False 
               mime_types:
                 - text/plain
               header_regexp: "^\\\\d+\\\\)(.+)"
               record_regexp: "([^ ]+) (.+)"
               """,
               Response.from_dict({
                   "body": CUSTOM_PATTERN_BODY.encode('utf-8'),
                   "encoding": 'utf-8',
                   "text": CUSTOM_PATTERN_BODY,
                   "headers": {
                       "content-type": "text/plain; charset=utf-8"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
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
                         mime_types:
                           - text/plain
                         """,
                         Response.from_dict({
                             "body": NO_END_LINEBREAK_BODY.encode('utf-8'),
                             "encoding": 'utf-8',
                             "text": NO_END_LINEBREAK_BODY,
                             "headers": {
                                 "content-type": "text/plain; charset=utf-8"
                             },
                             "url": "http://test",
                             "status_code": 200,
                             "elapsed": datetime.timedelta(seconds=1)
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
            NORMAL_CASE,
            CUSTOM_PATTERN,
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
