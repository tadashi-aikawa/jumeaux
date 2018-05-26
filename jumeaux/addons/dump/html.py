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


def pretty(html: str) -> str:
    return BeautifulSoup(html, "lxml").html.prettify()


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        encoding: str = payload.encoding.get_or(self.config.default_encoding)

        if self.config.force:
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        elif payload.response.type == 'html':
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        else:
            body = payload.body

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": body,
            "encoding": encoding
        })

