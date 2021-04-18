# -*- coding:utf-8 -*-
from owlmixin import OwlMixin, TOption, TList

from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.utils import when_optional_filter
from jumeaux.logger import Logger
from jumeaux.models import Res2ResAddOnPayload, Response, Request

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2res/type]"


class Condition(OwlMixin):
    type: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


def apply_first_condition(res: Response, req: Request, conditions: TList[Condition]) -> Response:
    condition: TOption[Condition] = conditions.find(
        lambda c: when_optional_filter(c.when, {'req': req.to_dict(), 'res': res.to_dict()})
    )
    if condition.is_none():
        return res

    return Response.from_dict(
        {
            "body": res.body,
            "type": condition.get().type,
            "encoding": res.encoding.get(),
            "headers": res.headers,
            "url": res.url,
            "status_code": res.status_code,
            "elapsed": res.elapsed,
            "elapsed_sec": res.elapsed_sec,
        },
    )


class Executor(Res2ResExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        return Res2ResAddOnPayload.from_dict({
            "req": payload.req,
            "response": apply_first_condition(payload.response, payload.req, self.config.conditions),
            "tags": payload.tags,
        })
