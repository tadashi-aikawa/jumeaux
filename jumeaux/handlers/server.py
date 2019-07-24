#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socketserver
import urllib
from http.server import SimpleHTTPRequestHandler
from typing import Optional

from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class MyServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        logger.info_lv2("*" * 80)
        logger.info_lv2("<<< Request headers >>>")
        logger.info_lv2(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logger.info_lv2("*" * 80)
        logger.info_lv2("<<< Request headers >>>")
        logger.info_lv2(self.headers)

        content_type = self.headers.get_content_type()
        content_charset = self.headers.get_content_charset() or "utf-8"

        if content_type == "application/x-www-form-urlencoded":
            logger.info_lv2("<<< Parse as x-www-form-urlencoded.. >>>")
            logger.info_lv2(
                urllib.parse.parse_qs(
                    self.rfile.read(int(self.headers.get("content-length"))).decode(
                        content_charset
                    ),
                    keep_blank_values=1,
                )
            )
        elif content_type == "application/json":
            logger.info_lv2(
                json.loads(
                    self.rfile.read(int(self.headers.get("content-length"))),
                    encoding=content_charset,
                )
            )

        SimpleHTTPRequestHandler.do_GET(self)


class ReuseAddressTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def handle(port: Optional[int]):
    with ReuseAddressTCPServer(("", port), MyServerHandler) as httpd:
        logger.info_lv1(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/)")
        httpd.serve_forever()
