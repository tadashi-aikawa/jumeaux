#!/usr/bin/env python
# -*- coding: utf-8 -*-

from livereload import Server
from jumeaux.logger import Logger
logger: Logger = Logger(__name__)


def reload():
    logger.info_lv1(f'Reload viewer.')


def handle(responses_dir: str, port: int):
    server = Server()
    server.watch(f'{responses_dir}/latest/report.json', reload)
    server.serve(root=f'{responses_dir}/latest', port=port, restart_delay=0, open_url_delay=1, open_url=True)

