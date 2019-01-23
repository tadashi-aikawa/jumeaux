# -*- coding:utf-8 -*-


import ast
import re
from typing import Any

import pydash as py_
from jinja2 import Environment, BaseLoader
from owlmixin import TOption


def exact_match(target: str, regexp: str):
    return bool(re.search(f'^{regexp}$', target))


def get_by_diff_key(dic: dict, diff_key: str) -> Any:
    return py_.get(dic, diff_key
                   .replace("root", "")
                   .replace("><", ".")
                   .replace(">", "")
                   .replace("<", "")
                   .replace("'", ""))


ENV = Environment(loader=BaseLoader())
ENV.filters['reg'] = exact_match


def when_filter(when: str, data: dict) -> bool:
    return ast.literal_eval(ENV.from_string('{{' + when + '}}').render(data))


def when_optional_filter(when: TOption[str], data: dict) -> bool:
    return when.map(lambda x: when_filter(x, data)).get_or(True)


def jinja2_format(fmt: str, data: dict) -> str:
    return ENV.from_string(fmt).render(data)
