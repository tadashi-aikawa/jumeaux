#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import namedtuple

import pytest
from owlmixin import TOption

from jumeaux.models import Proxy, Response


class TestProxy:
    def test_from_host_normal(self):
        actual = Proxy.from_host(TOption("proxy.net"))
        assert actual.http == "http://proxy.net"
        assert actual.https == "https://proxy.net"

    def test_from_host_none(self):
        actual = Proxy.from_host(TOption(None))
        assert actual is None


class TestModels:
    @pytest.mark.parametrize(
        'title, headers, text, content, encoding, apparent_encoding, expected', [
            ('Use encoding if charset exists.',
             {'content-type': 'application/xml;charset=UTF-8'},
             '<?xml version="1.0" encoding="Shift_JIS" ?>',
             '<?xml version="1.0" encoding="Shift_JIS" ?>'.encode('Shift_JIS'),
             'UTF-8', 'EUC_JP', 'UTF-8'),
            ('Use encoding if charset exists even if it is ISO-8859-1.',
             {'content-type': 'application/xml;charset=ISO-8859-1'},
             '<?xml version="1.0" encoding="Shift_JIS" ?>',
             '<?xml version="1.0" encoding="Shift_JIS" ?>'.encode('EUC_JP'),
             'ISO-8859-1', 'EUC_JP', 'ISO-8859-1'),
            ('Use encoding if charset does not exists.',
             {'content-type': 'application/xml'},
             '<?xml version="1.0" encoding="Shift_JIS" ?>',
             '<?xml version="1.0" encoding="Shift_JIS" ?>'.encode('EUC_JP'),
             None, 'EUC_JP', 'Shift_JIS'),
            ('Use meta-encoding if charset does not exists and mime-type is text/* and encoding is ISO-8859-1',
             {'content-type': 'text/xml'},
             '<?xml version="1.0" encoding="Shift_JIS" ?>',
             '<?xml version="1.0" encoding="Shift_JIS" ?>'.encode('EUC_JP'),
             'ISO-8859-1', 'EUC_JP', 'Shift_JIS'),
            ('Use apparent-encoding if charset does not exists and mime-type is text/* and encoding is ISO-8859-1 but meta-encoding does not exists',
             {'content-type': 'text/xml'},
             '<?xml version="1.0"?>',
             '<?xml version="1.0"?>'.encode('EUC_JP'),
             'ISO-8859-1', 'EUC_JP', 'EUC_JP'),
        ]
    )
    def test_from_requests_decide_encoding(self, title, headers, text, content, encoding, apparent_encoding, expected):
        Requests = namedtuple('Requests', ('headers', 'text', 'content', 'encoding', 'apparent_encoding'))

        actual = Response._decide_encoding(
            Requests(headers, text, content, encoding, apparent_encoding)
        )

        assert actual == expected
