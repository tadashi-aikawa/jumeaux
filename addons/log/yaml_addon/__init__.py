# -*- coding:utf-8 -*-

import urllib.parse as urlparser
import logging

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request, LogAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, encoding='utf8'):
        self.encoding: str = encoding


class Executor:
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: LogAddOnPayload) -> TList[Request]:
        """Transform from yaml to Request
    
        Exception:
            ValueError: If path does not exist.
        """
        try:
            return Request.from_yamlf_to_list(payload.file, encoding=self.config.encoding)
        except TypeError as e:
            raise ValueError(e)
