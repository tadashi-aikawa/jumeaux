# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import math
import ast
import re
from typing import Any

import pydash as py_
from jinja2 import Environment, BaseLoader
from jinja2.exceptions import TemplateSyntaxError
from owlmixin import TOption
from tzlocal import get_localzone


LOCAL_ZONE = get_localzone()


def exact_match(target: str, regexp: str) -> bool:
    return bool(re.search(f"^({regexp})$", target))


def now():
    return datetime.now(LOCAL_ZONE)


def mill_seconds_until(from_: datetime) -> float:
    dt = now() - from_
    return dt.seconds * 1000 + dt.microseconds / 1000


def to_jumeaux_xpath(xpath: str):
    return xpath.replace("[", "<").replace("]", ">")


def get_by_diff_key(dic: dict, diff_key: str) -> Any:
    return py_.get(
        dic,
        diff_key.replace("root", "")
        .replace("><", ".")
        .replace(">", "")
        .replace("<", "")
        .replace("'", ""),
    )


def calc_distance_km(
    wgs84_deg_lat1: float, wgs84_deg_lon1: float, wgs84_deg_lat2: float, wgs84_deg_lon2: float
) -> float:
    R = 6371
    rad1 = math.radians(wgs84_deg_lat1)
    rad2 = math.radians(wgs84_deg_lat2)
    delta_lat_rad = math.radians(wgs84_deg_lat2 - wgs84_deg_lat1)
    delta_lon_rad = math.radians(wgs84_deg_lon2 - wgs84_deg_lon1)

    a = math.sin(delta_lat_rad / 2) * math.sin(delta_lat_rad / 2) + math.cos(rad1) * math.cos(
        rad2
    ) * math.sin(delta_lon_rad / 2) * math.sin(delta_lon_rad / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


ENV = Environment(loader=BaseLoader())
ENV.filters["reg"] = exact_match
ENV.globals["calc_distance_km"] = calc_distance_km


def when_filter(when: str, data: dict) -> bool:
    return ast.literal_eval(ENV.from_string("{{" + when + "}}").render(data))


def when_optional_filter(when: TOption[str], data: dict) -> bool:
    return when.map(lambda x: when_filter(x, data)).get_or(True)


def jinja2_format(fmt: str, data: dict) -> str:
    return ENV.from_string(fmt).render(data)


def get_jinja2_format_error(fmt: str) -> TOption[str]:
    try:
        ENV.from_string(fmt)
        return TOption(None)
    except TemplateSyntaxError as err:
        return TOption(err.message)


def parse_datetime_dsl(value: str):
    m = re.search(r"^\$DATETIME\((.+)\)\((.+)\)$", value)
    return (now() + timedelta(seconds=int(m[2]))).strftime(m[1]) if m else value
