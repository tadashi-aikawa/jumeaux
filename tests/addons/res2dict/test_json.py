#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2dict.json import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

NORMAL_BODY = json.dumps({
    "total": 10,
    "items": [
        {"id": 1, "name": "Ichiro", "favorites": ["apple", "orange"]},
        {"id": 2, "name": "次郎"}
    ]
}, ensure_ascii=False)

ARRAY_TOP_BODY = json.dumps(["一郎", "Jiro"], ensure_ascii=False)

NORMAL_CASE = ("Normal",
               """
               force: False 
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "type": "json",
                   "encoding": 'euc-jp',
                   "headers": {
                       "content-type": "application/json; charset=utf-8"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               {
                   "total": 10,
                   "items": [
                       {
                           "id": 1,
                           "name": "Ichiro",
                           "favorites": ["apple", "orange"]
                       },
                       {
                           "id": 2,
                           "name": "次郎"
                       }
                   ]
               }
               )

ARRAY_TOP_CASE = ("Array top",
                  """
                  force: False 
                  """,
                  Response.from_dict({
                      "body": ARRAY_TOP_BODY.encode('utf8'),
                      "type": "json",
                      "encoding": 'utf8',
                      "headers": {
                          "content-type": "application/json; charset=utf-8"
                      },
                      "url": "http://test",
                      "status_code": 200,
                      "elapsed": datetime.timedelta(seconds=1)
                  }),
                  ["一郎", "Jiro"]
                  )

EMPTY_ENCODING_CASE = ("Encoding is empty (Decode as utf8)",
                       """
                       force: False 
                       """,
                       Response.from_dict({
                           "body": NORMAL_BODY.encode('euc-jp'),
                           "type": "json",
                           "headers": {
                               "content-type": "application/json; charset=utf-8"
                           },
                           "url": "http://test",
                           "status_code": 200,
                           "elapsed": datetime.timedelta(seconds=1)
                       }),
                       {
                           "total": 10,
                           "items": [
                               {
                                   "id": 1,
                                   "name": "Ichiro",
                                   "favorites": ["apple", "orange"]
                               },
                               {
                                   "id": 2,
                                   "name": "��Ϻ"
                               }
                           ]
                       }
                       )

NOT_JSON_CASE = ("Response is not json",
                 """
                 force: False 
                 """,
                 Response.from_dict({
                     "body": NORMAL_BODY.encode('utf8'),
                     "type": "xml",
                     "encoding": 'utf8',
                     "headers": {
                         "content-type": "bad/xml; charset=utf-8"
                     },
                     "url": "http://test",
                     "status_code": 200,
                     "elapsed": datetime.timedelta(seconds=1)
                 }),
                 None
                 )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, expected_result', [
            NORMAL_CASE,
            ARRAY_TOP_CASE,
            EMPTY_ENCODING_CASE,
            NOT_JSON_CASE,
        ]
    )
    def test(self, title, config_yml, response, expected_result):
        payload: Res2DictAddOnPayload = Res2DictAddOnPayload.from_dict({
            'response': response,
        })

        actual: Res2DictAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert actual.response == response
        assert actual.result.get() == expected_result
