# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.logger import Logger
from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.utils import when_optional_filter, jinja2_format, get_jinja2_format_error
from jumeaux.domain.config.vo import Config as JumeauxConfig
from jumeaux.models import Request, Reqs2ReqsAddOnPayload

logger: Logger = Logger(__name__)
LOG_PREFIX = "[reqs2reqs/rename]"


class Condition(OwlMixin):
    name: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


def apply_first_condition(request: Request, conditions: TList[Condition]) -> Request:
    condition: TOption[Condition] = conditions.find(
        lambda c: when_optional_filter(c.when, request.to_dict())
    )
    if condition.is_none():
        return request

    name: TOption[str] = jinja2_format(
        condition.get().name, request.to_dict()
    ) if when_optional_filter(condition.get().when, request.to_dict()) else request.name

    return Request.from_dict({**request.to_dict(), "name": name})


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

        errors: TList[str] = self.config.conditions.reject(lambda x: x.when.is_none()).map(
            lambda x: get_jinja2_format_error(x.when.get()).get()
        ).filter(lambda x: x is not None)
        if errors:
            logger.error(f"{LOG_PREFIX} Illegal format in `conditions[*].when`.")
            logger.error(f"{LOG_PREFIX} Please check your configuration yaml files.")
            logger.error(f"{LOG_PREFIX} --- Error messages ---")
            errors.map(lambda x: logger.error(f"{LOG_PREFIX}   * `{x}`"))
            logger.error(f"{LOG_PREFIX} ---------------------", exit=True)

    def exec(self, payload: Reqs2ReqsAddOnPayload, config: JumeauxConfig) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict(
            {
                "requests": payload.requests.map(
                    lambda r: apply_first_condition(r, self.config.conditions)
                )
            }
        )
