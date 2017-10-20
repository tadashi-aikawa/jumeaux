#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import pytest

from owlmixin.util import load_yaml, dump_json, load_json

from jumeaux.addons.res2dict.xml import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

NORMAL_BODY = """<?xml version="1.0"?>
<catalog>
    <book id="bk001">
        <author>Ichiro</author>
        <title>Ichiro55</title>
    </book>
    <book id="bk002">
        <author>次郎</author>
        <title>次郎22</title>
    </book>
</catalog>
"""

NORMAL_CASE = ("Normal",
               """
               force: False 
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "encoding": 'euc-jp',
                   "text": NORMAL_BODY,
                   "headers": {
                       "content-type": "application/xml"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               {
                   "catalog": {
                       "book": [
                           {"@id": "bk001", "author": "Ichiro", "title": "Ichiro55"},
                           {"@id": "bk002", "author": "次郎", "title": "次郎22"}
                       ]
                   }
               }
               )

EMPTY_ENCODING_CASE = ("Encoding is empty",
                       """
                       force: False 
                       """,
                       Response.from_dict({
                           "body": NORMAL_BODY.encode('euc-jp'),
                           "text": NORMAL_BODY,
                           "headers": {
                               "content-type": "application/xml"
                           },
                           "url": "http://test",
                           "status_code": 200,
                           "elapsed": datetime.timedelta(seconds=1)
                       }),
                       {
                           "catalog": {
                               "book": [
                                   {"@id": "bk001", "author": "Ichiro", "title": "Ichiro55"},
                                   {"@id": "bk002", "author": "次郎", "title": "次郎22"}
                               ]
                           }
                       }
                       )

INVALID_CONTENT_TYPE_CASE = ("Content type is invalid",
               """
               force: False 
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "encoding": 'euc-jp',
                   "text": NORMAL_BODY,
                   "headers": {
                       "content-type": "hogehoge"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               None
               )

INVALID_CONTENT_TYPE_BUT_FORCE_CASE = ("Content type is invalid but force",
               """
               force: True 
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "encoding": 'euc-jp',
                   "text": NORMAL_BODY,
                   "headers": {
                       "content-type": "hogehoge"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               {
                   "catalog": {
                       "book": [
                           {"@id": "bk001", "author": "Ichiro", "title": "Ichiro55"},
                           {"@id": "bk002", "author": "次郎", "title": "次郎22"}
                       ]
                   }
               }
               )

class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, expected_result', [
            NORMAL_CASE,
            EMPTY_ENCODING_CASE,
            INVALID_CONTENT_TYPE_CASE,
            INVALID_CONTENT_TYPE_BUT_FORCE_CASE,
        ]
    )
    def test(self, title, config_yml, response, expected_result):
        payload: Res2DictAddOnPayload = Res2DictAddOnPayload.from_dict({
            'response': response,
        })

        actual: Res2DictAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert actual.response == response
        assert load_json(dump_json(actual.result.get())) == expected_result
