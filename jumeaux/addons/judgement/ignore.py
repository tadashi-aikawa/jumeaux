# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList, TDict

from jumeaux.addons.judgement import JudgementExecutor
from jumeaux.addons.utils import exact_match, when_optional_filter, jinja2_format, get_jinja2_format_error, \
    get_by_diff_key
from jumeaux.logger import Logger
from jumeaux.models import JudgementAddOnPayload, DiffKeys, JudgementAddOnReference

logger: Logger = Logger(__name__)
LOG_PREFIX = "[judgement/ignore]"


class Case(OwlMixin):
    path: str
    when: TOption[str]


class Condition(OwlMixin):
    when: TOption[str]
    added: TList[Case] = []
    removed: TList[Case] = []
    changed: TList[Case] = []


class Ignore(OwlMixin):
    title: str
    conditions: TList[Condition]


class Config(OwlMixin):
    ignores: TList[Ignore]


def match(path: str, case: Case, one: dict, other: dict) -> bool:
    return exact_match(path, case.path) and when_optional_filter(case.when, {
        "one": get_by_diff_key(one, path),
        "other": get_by_diff_key(other, path),
    })


def to_matched_unknown(unknown_diff: DiffKeys, condition: Condition, ref: JudgementAddOnReference) -> DiffKeys:
    return DiffKeys.from_dict({
        "added": unknown_diff.added.filter(
            lambda path: condition.added.any(lambda case: match(path, case, ref.dict_one.get(), ref.dict_other.get()))
        ),
        "removed": unknown_diff.removed.filter(
            lambda path: condition.removed.any(lambda case: match(path, case, ref.dict_one.get(), ref.dict_other.get()))
        ),
        "changed": unknown_diff.changed.filter(
            lambda path: condition.changed.any(lambda case: match(path, case, ref.dict_one.get(), ref.dict_other.get()))
        )
    })


def merge_diff_keys(diffs_by_cognition: TDict[DiffKeys], matched_unknown: DiffKeys, title: str) -> TDict[DiffKeys]:
    unknown = DiffKeys.from_dict({
        "added": diffs_by_cognition["unknown"].added.reject(lambda x: x in matched_unknown.added),
        "removed": diffs_by_cognition["unknown"].removed.reject(lambda x: x in matched_unknown.removed),
        "changed": diffs_by_cognition["unknown"].changed.reject(lambda x: x in matched_unknown.changed),
    })

    merged: DiffKeys = matched_unknown if title not in diffs_by_cognition else \
        DiffKeys.from_dict({
            "added": diffs_by_cognition[title].added.concat(matched_unknown.added),
            "removed": diffs_by_cognition[title].removed.concat(matched_unknown.removed),
            "changed": diffs_by_cognition[title].changed.concat(matched_unknown.changed),
        })

    return diffs_by_cognition.assign({
        "unknown": unknown,
        title: merged,
    })


def fold_diffs_by_cognition(diffs_by_cognition: TDict[DiffKeys], ignore: Ignore, ref: JudgementAddOnReference) -> TDict[DiffKeys]:
    matched_unknowns: TList[DiffKeys] = ignore.conditions \
        .filter(lambda c: when_optional_filter(c.when, {
            "req": {
                "name": ref.name,
                "path": ref.path,
                "qs": ref.qs,
                "headers": ref.headers,
            },
            "res_one": ref.res_one,
            "res_other": ref.res_other,
            "dict_one": ref.dict_one,
            "dict_other": ref.dict_other,
        })) \
        .map(lambda cond: to_matched_unknown(diffs_by_cognition["unknown"], cond, ref))

    return matched_unknowns.reduce(lambda t, x: merge_diff_keys(t, x, ignore.title), diffs_by_cognition)


def validate_config(config: Config):
    errors: TList[str] = config.ignores \
        .flat_map(lambda x: x.conditions) \
        .reject(lambda x: x.when.is_none()) \
        .map(lambda x: get_jinja2_format_error(x.when.get()).get()) \
        .filter(lambda x: x is not None)
    if errors:
        logger.error(f"{LOG_PREFIX} Illegal format in `conditions[*].when`.")
        logger.error(f"{LOG_PREFIX} Please check your configuration yaml files.")
        logger.error(f"{LOG_PREFIX} --- Error messages ---")
        errors.map(lambda x: logger.error(f"{LOG_PREFIX}   * `{x}`"))
        logger.error(f"{LOG_PREFIX} ---------------------", exit=True)
    # TODO: added, changed, removed...


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})
        validate_config(self.config)

    def exec(self, payload: JudgementAddOnPayload, reference: JudgementAddOnReference) -> JudgementAddOnPayload:
        if payload.regard_as_same or payload.diffs_by_cognition.is_none():
            return payload

        diffs_by_cognition = self.config.ignores \
            .reduce(lambda t, x: fold_diffs_by_cognition(t, x, reference), payload.diffs_by_cognition.get()) \

        logger.debug(f"{LOG_PREFIX} ----- [START] diffs by cognition")
        logger.debug(diffs_by_cognition.to_pretty_json())
        logger.debug(f"{LOG_PREFIX} ----- [END] diffs by cognition")

        return JudgementAddOnPayload.from_dict({
            "diffs_by_cognition": diffs_by_cognition.omit_by(lambda k, v: v.is_empty()),
            "regard_as_same": diffs_by_cognition["unknown"].is_empty(),
        })
