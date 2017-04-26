# -*- coding:utf-8 -*-

import logging

from owlmixin import OwlMixin
from xml.dom import minidom
from xml.etree import ElementTree

from jumeaux.addons.dump import DumpExecutor
from jumeaux.models import DumpAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, default_encoding: str ='utf8', force=False):
        self.default_encoding: str = default_encoding
        self.force: bool = force


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

    def exec(self, payload: DumpAddOnPayload):
        content_type = payload.response.headers.get('content-type')
        mime_type = content_type.split(';')[0] if content_type else None
        encoding = payload.encoding or self.config.default_encoding

        if self.config.force:
            logger.debug(f"Forced to xml -- mime_type: {mime_type} -- encoding: {encoding}")
            body = pretty(payload.body.decode(encoding)).encode(encoding)
        elif mime_type in ('text/xml', 'application/xml'):
            logger.debug(f"Parse as xml -- mime_type: {mime_type} -- encoding: {encoding}")
            body = pretty(payload.body.decode(encoding)).encode(encoding)
        else:
            body = payload.body

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": body,
            "encoding": encoding
        })
