# -*- coding:utf-8 -*-

from xml.dom import minidom
from xml.etree import ElementTree

from owlmixin import OwlMixin, TList

from jumeaux.addons.dump import DumpExecutor
from jumeaux.logger import Logger
from jumeaux.models import DumpAddOnPayload

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    default_encoding: str = 'utf8'
    force: bool = False


def pretty(xmls: str) -> str:
    try:
        tree = ElementTree.XML(xmls)
        logger.debug("Success to parsing xml")
        return minidom.parseString(ElementTree.tostring(tree)).toprettyxml(indent='    ')
    except ElementTree.ParseError:
        logger.warning("Fail to parsing xml")
        return f"""Include invalid token

        {xmls}
        """


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        encoding: str = payload.encoding.get_or(self.config.default_encoding)

        if self.config.force:
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        elif payload.response.type == 'xml':
            body = pretty(payload.body.decode(encoding, errors='replace')).encode(encoding, errors='replace')
        else:
            body = payload.body

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": body,
            "encoding": encoding
        })
