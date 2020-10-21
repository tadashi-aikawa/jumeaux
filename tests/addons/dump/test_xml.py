#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import os
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.dump.xml import Executor
from jumeaux.models import Response, DumpAddOnPayload

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
""".replace('\n', '').replace('    ', '')

CORRUPTION_BODY_BYTES: bytes = '<?xml version="1.0"?><catalog><book><title>ゆーてぃーえふ</title></book>'.encode(
    'utf8') + '<book><title>いーゆーしー</title></book></catalog>'.encode('euc-jp')

NORMAL_CASE = ("Normal",
               """
               force: False
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "type": "xml",
                   "encoding": 'euc-jp',
                   "headers": {
                       "content-type": "application/xml; charset=euc-jp"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1),
                   "elapsed_sec": 1.0,
               }),
               NORMAL_BODY.encode('euc-jp'),
               'euc-jp',
               """<?xml version="1.0" ?>
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
""".encode('euc-jp'),
               'euc-jp'
               )

CORRUPTION_CASE = ("Corruption",
                   """
                   force: False
                   """,
                   Response.from_dict({
                       "body": CORRUPTION_BODY_BYTES,
                       "type": "xml",
                       "encoding": 'euc-jp',
                       "headers": {
                           "content-type": "application/xml; charset=euc-jp"
                       },
                       "url": "http://test",
                       "status_code": 200,
                       "elapsed": datetime.timedelta(seconds=1),
                       "elapsed_sec": 1.0,
                   }),
                   CORRUPTION_BODY_BYTES,
                   'euc-jp',
                   """<?xml version="1.0" ?>
<catalog>
    <book>
        <title>�����若�������若�����</title>
    </book>
    <book>
        <title>いーゆーしー</title>
    </book>
</catalog>
""".encode('euc-jp', errors='replace'),
                   'euc-jp'
                   )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, body, encoding, expected_body, expected_encoding', [
            NORMAL_CASE,
            CORRUPTION_CASE,
        ]
    )
    def test(self, title, config_yml, response, body, encoding, expected_body, expected_encoding):
        payload: DumpAddOnPayload = DumpAddOnPayload.from_dict({
            'response': response,
            'body': body,
            'encoding': encoding,
        })

        actual: DumpAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert actual.body == expected_body
        assert actual.encoding.get() == expected_encoding
