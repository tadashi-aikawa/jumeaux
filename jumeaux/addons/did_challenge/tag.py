# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption, TList, TDict

from jumeaux.addons.did_challenge import DidChallengeExecutor
from jumeaux.utils import when_optional_filter, jinja2_format, get_jinja2_format_error
from jumeaux.logger import Logger
from jumeaux.models import DidChallengeAddOnPayload, DidChallengeAddOnReference, Trial

logger: Logger = Logger(__name__)
LOG_PREFIX = "[did_challenge/tag]"


class Condition(OwlMixin):
    tag: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


class Executor(DidChallengeExecutor):
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

    def exec(
        self, payload: DidChallengeAddOnPayload, referenece: DidChallengeAddOnReference
    ) -> DidChallengeAddOnPayload:
        def to_dict(trial: Trial) -> TDict:
            return TDict(
                {
                    "trial": trial.to_dict(),
                    "res_one": referenece.res_one.to_dict(),
                    "res_other": referenece.res_other.to_dict(),
                    "res_one_props": referenece.res_one_props.get(),
                    "res_other_props": referenece.res_other_props.get(),
                }
            )

        # TODO: remove TOption (owlmixin... find)
        conditions: TList[Condition] = self.config.conditions.filter(
            lambda c: when_optional_filter(c.when, to_dict(payload.trial))
        )
        if not conditions:
            logger.debug(f"{LOG_PREFIX} There are no matched conditions")
            return payload

        tags: TList[str] = conditions.reduce(
            lambda t, x: t + [jinja2_format(x.tag, to_dict(payload.trial))], payload.trial.tags
        )
        return DidChallengeAddOnPayload.from_dict(
            {"trial": Trial.from_dict({**payload.trial.to_dict(), "tags": tags})}
        )
