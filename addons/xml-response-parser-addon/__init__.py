# -*- coding:utf-8 -*-

from xml.dom import minidom
from xml.etree import ElementTree
from owlmixin import OwlMixin
from modules.models import ResponseAddOnPayload


class Config(OwlMixin):
    def __init__(self, force=False):
        self.force: bool = force


def main(payload: ResponseAddOnPayload, config_dict: dict):
    config: Config = Config.from_dict(config_dict or {})
    content_type = payload.response.headers.get('content-type')
    mime_type = content_type.split(';')[0] if content_type else None

    return ResponseAddOnPayload.from_dict({
        "response": payload.response,
        "body": minidom.parseString(
            ElementTree.tostring(ElementTree.XML(payload.body.decode(payload.encoding)))
        ).toprettyxml(indent='    ')
        .encode(payload.encoding) if config.force or mime_type in ('text/xml', 'application/xml') else payload.body,
        "encoding": payload.encoding
    })
