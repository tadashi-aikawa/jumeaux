# -*- coding:utf-8 -*-

import json
from xml.dom import minidom
from xml.etree import ElementTree


def divide_content_type(headers):
    """
    :param headers:
    :return: mime_type, encoding
    """
    content_type = headers.get('content-type')
    if not content_type:
        return None

    ll = content_type.split(';')
    return ll[0], ll[1] if len(ll) > 1 else None


def main(res, config):
    mime_type, encoding = divide_content_type(res.headers)
    text = res.content.decode(encoding or 'utf8')

    if mime_type in ('text/json', 'application/json'):
        return json.dumps(json.loads(text), ensure_ascii=False, indent=4, sort_keys=True)
    elif mime_type in ('text/xml', 'application/xml'):
        try:
            tree = ElementTree.XML(text)
            return minidom.parseString(ElementTree.tostring(tree)).toprettyxml(indent='    ')
        except:
            return "Invalid....!!"
    else:
        # TODO: If binary, return res.content or None
        return res.text
