# -*- coding:utf-8 -*-

from xml.dom import minidom
from xml.etree import ElementTree
from owlmixin import OwlMixin
from modules.models import ResponseAddOnPayload
import logging

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, default_encoding='utf8', force=False):
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


def exec(payload: ResponseAddOnPayload, config_dict: dict):
    config: Config = Config.from_dict(config_dict or {})
    content_type = payload.response.headers.get('content-type')
    mime_type = content_type.split(';')[0] if content_type else None
    encoding = payload.encoding or config.default_encoding

    if config.force:
        logger.debug(f"Forced to xml -- mime_type: {mime_type} -- encoding: {encoding}")
        body = pretty(payload.body.decode(encoding)).encode(encoding)
    elif mime_type in ('text/xml', 'application/xml'):
        logger.debug(f"Parse as xml -- mime_type: {mime_type} -- encoding: {encoding}")
        body = pretty(payload.body.decode(encoding)).encode(encoding)
    else:
        body = payload.body

    return ResponseAddOnPayload.from_dict({
        "response": payload.response,
        "body": body,
        "encoding": encoding
    })
