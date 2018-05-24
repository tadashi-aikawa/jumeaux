#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.res2dict.html import Executor
from jumeaux.models import Response, Res2DictAddOnPayload

NORMAL_BODY = """<!DOCTYPE html>
<html>
<head>
  <title>タイトル</title>
  <meta name="format-detection" content="telephone=no">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <script type="text/javascript" charset="utf-8">
    var hoge = 1 > 2;
  </script>
</head>
<body>
  <div id="main">
    <span>Main contents</span>
  </div>
</body>
</html>
"""

NORMAL_CASE = ("Normal",
               """
               force: False
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('utf8'),
                   "type": "html",
                   "encoding": 'utf8',
                   "headers": {
                       "content-type": "text/html"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               {
                   "html": {
                       "head": {
                           "title": {
                               "##value": "タイトル"
                           },
                           "meta": [
                               {
                                   "#name": "format-detection",
                                   "#content": "telephone=no",
                                   "##value": ""
                               },
                               {
                                   "#http-equiv": "Content-Type",
                                   "#content": "text/html; charset=utf-8",
                                   "##value": ""
                               }
                           ],
                           "script": {
                               "#type": "text/javascript",
                               "#charset": "utf-8",
                               "##value": "var hoge = 1 > 2;"
                           }
                       },
                       "body": {
                           "div": {
                               "#id": "main",
                               "span": {
                                   "##value": "Main contents"
                               }
                           }
                       }
                   }
               }
               )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, expected_result', [
            NORMAL_CASE,
        ]
    )
    def test(self, title, config_yml, response, expected_result):
        payload: Res2DictAddOnPayload = Res2DictAddOnPayload.from_dict({
            'response': response,
        })

        actual: Res2DictAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert response == actual.response
        assert expected_result == actual.result.get()
