# -*- coding:utf-8 -*-


import ast
import re
from typing import Any
from jinja2 import Environment, BaseLoader

import pydash as py_


def exact_match(target: str, regexp: str):
    return bool(re.search(f'^{regexp}$', target))


def get_by_diff_key(d: dict, diff_key: str) -> Any:
    return py_.get(d, diff_key
                   .replace("root", "")
                   .replace("><", ".")
                   .replace(">", "")
                   .replace("<", "")
                   .replace("'", ""))


env = Environment(loader=BaseLoader())
env.filters['reg'] = exact_match


def when_filter(when: str, data: dict) -> bool:
    return ast.literal_eval(env.from_string('{{' + when + '}}').render(data))

