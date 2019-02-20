# -*- coding:utf-8 -*-

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList, TDict

from jumeaux.addons.judgement import JudgementExecutor
from jumeaux.addons.utils import exact_match
from jumeaux.logger import Logger
from jumeaux.models import JudgementAddOnPayload, DiffKeys, JudgementAddOnReference

logger: Logger = Logger(__name__)
LOG_PREFIX = "[judgement/ignore_properties]"


# TODO: deprecated
class ConditionDeprecated(OwlMixin):
    name: TOption[str]
    path: TOption[str]
    added: TList[str] = []
    removed: TList[str] = []
    changed: TList[str] = []


# TODO: deprecated
class IgnoreDeprecated(OwlMixin):
    title: str
    conditions: TList[ConditionDeprecated]
    image: TOption[str]
    link: TOption[str]


def to_matched_unknown(unknown_diff: DiffKeys, condition: ConditionDeprecated, ref: JudgementAddOnReference) -> DiffKeys:
    if any([condition.path.get() and not exact_match(ref.path, condition.path.get()),
            condition.name.get() and not exact_match(ref.name, condition.name.get())]):
        return DiffKeys.empty()

    return DiffKeys.from_dict({
        "added": unknown_diff.added.filter(
            lambda dk: condition.added.any(lambda ig: exact_match(dk, ig))
        ),
        "removed": unknown_diff.removed.filter(
            lambda dk: condition.removed.any(lambda ig: exact_match(dk, ig))
        ),
        "changed": unknown_diff.changed.filter(
            lambda dk: condition.changed.any(lambda ig: exact_match(dk, ig))
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


def fold_diffs_by_cognition(diffs_by_cognition: TDict[DiffKeys], ignore: IgnoreDeprecated, ref: JudgementAddOnReference) -> TDict[DiffKeys]:
    matched_unknowns: TList[DiffKeys] = ignore.conditions.map(
        lambda cond: to_matched_unknown(diffs_by_cognition["unknown"], cond, ref)
    )
    return matched_unknowns.reduce(lambda t, x: merge_diff_keys(t, x, ignore.title), diffs_by_cognition)


class Config(OwlMixin):
    ignores: TList[IgnoreDeprecated]


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict) -> None:
        logger.warning(f"{LOG_PREFIX} This add-on will be removed soon.")
        logger.warning(f"{LOG_PREFIX} Please use `judgement/ignore` instead.")
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: JudgementAddOnPayload, reference: JudgementAddOnReference) -> JudgementAddOnPayload:
        if payload.regard_as_same or payload.diffs_by_cognition.is_none():
            return payload

        diffs_by_cognition = self.config.ignores \
            .reduce(lambda t, x: fold_diffs_by_cognition(t, x, reference), payload.diffs_by_cognition.get()) \

        logger.debug('-' * 80)
        logger.debug('filter_diff_keys')
        logger.debug('-' * 80)
        logger.debug(diffs_by_cognition.to_pretty_json())

        return JudgementAddOnPayload.from_dict({
            "diffs_by_cognition": diffs_by_cognition.omit_by(lambda k, v: v.is_empty()),
            "regard_as_same": diffs_by_cognition["unknown"].is_empty(),
        })
