# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from owlmixin import OwlMixin, TList

from jumeaux.addons.dump import DumpExecutor
from jumeaux.logger import Logger
from jumeaux.models import DumpAddOnPayload

logger: Logger = Logger(__name__)
LOG_PREFIX = "[dump/html]"


class Config(OwlMixin):
    default_encoding: str = 'utf8'
    force: bool = False
    mime_types: TList[str] = [
        'text/html'
    ]


def pretty(html: str) -> str:
    return BeautifulSoup(html, "lxml").html.prettify()


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        mime_type: str = payload.response.mime_type.get()
        encoding: str = payload.encoding.get_or(self.config.default_encoding)

        if self.config.force:
            logger.debug(f"{LOG_PREFIX} Forced to html -- mime_type: {mime_type} -- encoding: {encoding}")
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        elif mime_type in self.config.mime_types:
            logger.debug(f"{LOG_PREFIX} Parse as html -- mime_type: {mime_type} -- encoding: {encoding}")
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        else:
            logger.debug(f"{LOG_PREFIX} Don't Parse as html -- mime_type: {mime_type} -- encoding: {encoding}")
            body = payload.body

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": body,
            "encoding": encoding
        })

