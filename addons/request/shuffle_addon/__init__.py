# -*- coding:utf-8 -*-

import logging
import random

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from modules.models import Request

logger = logging.getLogger(__name__)


def exec(requests: TList[Request], config_dict: dict) -> TList[Request]:
    random.shuffle(requests)
    return requests
