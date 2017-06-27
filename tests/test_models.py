#!/usr/bin/env python
# -*- coding:utf-8 -*-
from owlmixin import TOption

from jumeaux.models import Proxy


class TestProxy:
    def test_from_host_normal(self):
        actual = Proxy.from_host(TOption("proxy.net"))
        assert actual.http == "http://proxy.net"
        assert actual.https == "https://proxy.net"

    def test_from_host_none(self):
        actual = Proxy.from_host(TOption(None))
        assert actual is None
