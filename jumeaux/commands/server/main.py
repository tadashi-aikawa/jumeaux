"""Boot mock API server
Usage:
  {cli} [--port <port>] [-v|-vv|-vvv]
  {cli} (-h | --help)

Options:
  --port <port>                 Running port [default: 8000]
  -v                            Logger level (`-v` or `-vv` or `-vvv`)
  -h --help                     Show this screen.
"""
import json
import socketserver
import urllib
from http.server import SimpleHTTPRequestHandler

from owlmixin import OwlMixin

from jumeaux.logger import Logger, init_logger

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


class Args(OwlMixin):
    port: int
    v: int


def run(args: Args):
    init_logger(args.v)
    with ReuseAddressTCPServer(("", args.port), MyServerHandler) as httpd:
        logger.info_lv1(f"Serving HTTP on 0.0.0.0 port {args.port} (http://0.0.0.0:{args.port}/)")
        httpd.serve_forever()
