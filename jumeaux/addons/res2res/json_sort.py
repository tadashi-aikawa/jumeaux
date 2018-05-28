# -*- coding:utf-8 -*-

import json
from typing import Any

from owlmixin import OwlMixin, TList, TOption

from jumeaux.addons.conditions import RequestCondition, AndOr
from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.addons.utils import exact_match
from jumeaux.models import Res2ResAddOnPayload, Response, Request
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2res/json_sort]"


class Target(OwlMixin):
    path: str
    sort_keys: TOption[TList[str]]


class Sorter(OwlMixin):
    conditions: TList[RequestCondition]
    and_or: AndOr = "and"  # type: ignore # Prevent for enum problem
    negative: bool = False
    targets: TList[Target]

    def fulfill(self, req: Request) -> bool:
        return self.negative ^ (self.and_or.check(self.conditions.map(lambda x: x.fulfill(req))))


class Config(OwlMixin):
    items: TList[Sorter]
    # TODO: remove
    default_encoding: TOption[str]


def traverse(value: Any, location: str, targets: TList[Target]):
    if isinstance(value, dict):
        return _dict_sort(value, targets, location)
    elif isinstance(value, list):
        return _list_sort(value, targets, location)
    else:
        return value


def _dict_sort(dict_obj: dict, targets: TList[Target], location: str = 'root') -> dict:
    return {k: traverse(v, f"{location}<'{k}'>", targets) for k, v in dict_obj.items()}


def _list_sort(list_obj: list, targets: TList[Target], location: str = 'root') -> list:
    target: Target = targets.find(lambda t: exact_match(location, t.path))

    traversed = [traverse(v, f"{location}<{i}>", targets) for i, v in enumerate(list_obj)]
    if not target:
        return traversed

    sort_func = target.sort_keys.map(lambda keys: lambda x: [x[k] for k in keys]) \
        .get_or(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)

    return sorted(traversed, key=sort_func)


class Executor(Res2ResExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})
        if self.config.default_encoding.get():
            logger.warning(f'{LOG_PREFIX} `default_encoding` is no longer works.')
            logger.warning(f'{LOG_PREFIX} And this will be removed soon! You need to remove this property not to stop!')

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        res: Response = payload.response

        if res.type != "json":
            logger.info_lv3(f"{LOG_PREFIX} Skipped because this response is not json.")
            return payload

        res_json = json.loads(res.text)
        sorted_res = json.dumps(
            self.config.items.reduce(lambda t, s:
                                     (_dict_sort(t, s.targets)
                                      if isinstance(t, dict)
                                      else _list_sort(t, s.targets))
                                     if s.fulfill(payload.req) else t, res_json),
            ensure_ascii=False
        )

        return Res2ResAddOnPayload.from_dict({
            "response": {
                "body": sorted_res.encode(res.encoding.get(), errors='replace'),
                "type": res.type,
                "encoding": res.encoding.get(),
                "headers": res.headers,
                "url": res.url,
                "status_code": res.status_code,
                "elapsed": res.elapsed,
                "elapsed_sec": res.elapsed_sec,
            },
            "req": payload.req,
        })
