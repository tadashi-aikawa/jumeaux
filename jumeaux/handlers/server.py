#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import SimpleHTTPRequestHandler
import socketserver

from typing import Optional

from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class MyServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        logger.info_lv2(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)


class ReuseAddressTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def handle(port: Optional[int]):
    with ReuseAddressTCPServer(("", port), MyServerHandler) as httpd:
        logger.info_lv1(f'Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/)')
        httpd.serve_forever()
