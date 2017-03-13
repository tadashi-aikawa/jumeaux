# -*- coding:utf-8 -*-

import urllib.parse as urlparser
import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding='utf8'):
        self.encoding: str = encoding


def main(file: str, config_dict: dict) -> TList[Request]:
    """Transform from yaml to Request

    Exception:
        ValueError: If path does not exist.
    """
    config: Config = Config.from_dict(config_dict or {})

    try:
        return Request.from_yamlf_to_list(file, encoding=config.encoding)
    except TypeError as e:
        raise ValueError(e)
