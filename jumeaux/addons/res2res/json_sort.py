# -*- coding:utf-8 -*-

import logging
import json
from owlmixin import OwlMixin, TList, TOption, TDict

from jumeaux.addons.conditions import RequestCondition, AndOr
from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.addons.utils import exact_match
from jumeaux.models import Res2ResAddOnPayload, Response, Request

logger = logging.getLogger(__name__)


class Target(OwlMixin):
    path: str
    sort_keys: TOption[TList[str]]


class Sorter(OwlMixin):
    conditions: TList[RequestCondition]
    and_or: AndOr = "and"
    negative: bool = False
    targets: TList[Target]

    def fulfill(self, req: Request) -> bool:
        return self.negative ^ (self.and_or.check(self.conditions.map(lambda x: x.fulfill(req))))


class Config(OwlMixin):
    items: TList[Sorter]
    default_encoding: str = 'utf8'


def traverse(value: any, location: str, targets: TList[Target]):
    if isinstance(value, dict):
        return _dict_sort(value, targets, location)
    elif isinstance(value, list):
        return _list_sort(value, targets, location)
    else:
        return value


def _dict_sort(dict_obj: dict, targets: TList[Target], location: str = 'root') -> dict:
    return {k: traverse(v, f"{location}<'{k}'>", targets) for k, v in dict_obj.items()}


def _list_sort(list_obj: list, targets: TList[Target], location: str = 'root') -> list:
    target: Target = targets.find(lambda t: exact_match(t.path, location))

    traversed = [traverse(v, f"{location}<{i}>", targets) for i, v in enumerate(list_obj)]
    if not target:
        return traversed

    sort_func = target.sort_keys.map(lambda keys: lambda x: [x[k] for k in keys]) \
        .get_or(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)

    return sorted(traversed, key=sort_func)


class Executor(Res2ResExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        res: Response = payload.response

        content_type = res.headers.get('content-type')
        mime_type = content_type.split(';')[0] if content_type else None

        if mime_type not in ('text/json', 'application/json'):
            logger.info("Skipped because mime type is not json.")
            return payload

        res_json = json.loads(res.text, encoding=res.encoding)
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
                "body": sorted_res.encode(res.encoding.get_or(self.config.default_encoding)),
                "encoding": res.encoding.get(),
                "text": sorted_res,
                "headers": res.headers,
                "url": res.url,
                "status_code": res.status_code,
                "elapsed": res.elapsed,
            },
            "req": payload.req,
        })
