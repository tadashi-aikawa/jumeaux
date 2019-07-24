# -*- coding:utf-8 -*-

import json
from typing import Any

from owlmixin import OwlMixin, TList, TOption

from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.addons.utils import exact_match, when_filter
from jumeaux.logger import Logger
from jumeaux.models import Res2ResAddOnPayload, Response

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2res/json_sort]"


class Target(OwlMixin):
    path: str
    sort_keys: TOption[TList[str]]


class Sorter(OwlMixin):
    when: str
    targets: TList[Target]


class Config(OwlMixin):
    items: TList[Sorter]
    footprints_tag: TOption[str]


def traverse(value: Any, location: str, targets: TList[Target]):
    if isinstance(value, dict):
        return _dict_sort(value, targets, location)
    if isinstance(value, list):
        return _list_sort(value, targets, location)
    return value


def _dict_sort(dict_obj: dict, targets: TList[Target], location: str = "root") -> dict:
    return {k: traverse(v, f"{location}<'{k}'>", targets) for k, v in dict_obj.items()}


def _list_sort(list_obj: list, targets: TList[Target], location: str = "root") -> list:
    target: TOption[Target] = targets.find(lambda t: exact_match(location, t.path))

    traversed = [traverse(v, f"{location}<{i}>", targets) for i, v in enumerate(list_obj)]
    if target.is_none():
        return traversed

    sort_func = (
        target.get()
        .sort_keys.map(lambda keys: lambda x: [x[k] for k in keys])
        .get_or(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)
    )

    return sorted(traversed, key=sort_func)


class Executor(Res2ResExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        res: Response = payload.response

        if res.type != "json":
            logger.info_lv3(f"{LOG_PREFIX} Skipped because this response is not json.")
            return payload

        res_json = json.loads(res.text)
        res_json_sorted = self.config.items.reduce(
            lambda t, s: (
                _dict_sort(t, s.targets) if isinstance(t, dict) else _list_sort(t, s.targets)
            )
            if when_filter(s.when, payload.req.to_dict())
            else t,
            res_json,
        )

        return Res2ResAddOnPayload.from_dict(
            {
                "response": {
                    "body": json.dumps(res_json_sorted, ensure_ascii=False).encode(
                        res.encoding.get(), errors="replace"
                    ),
                    "type": res.type,
                    "encoding": res.encoding.get(),
                    "headers": res.headers,
                    "url": res.url,
                    "status_code": res.status_code,
                    "elapsed": res.elapsed,
                    "elapsed_sec": res.elapsed_sec,
                },
                "req": payload.req,
                "tags": payload.tags.concat(
                    self.config.footprints_tag.map(
                        lambda x: [x] if res_json != res_json_sorted else []
                    ).get_or([])
                ),
            }
        )
