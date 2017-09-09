# -*- coding:utf-8 -*-

import re


def exact_match(regexp: str, target: str):
    return bool(re.search(f'^{regexp}$', target))
