# -*- coding:utf-8 -*-

"""For example of config
judgement:
  - name: jumeaux.addons.judgement.ignore_properties
    config:
      ignores:
        - title: reason
          image: https://......png
          link: https://......
          conditions:
            - path: '/route'
              changed:
                - root['items'][0]
                - root['unit']
            - path: '/repositories'
              added:
                - root['items'][\d+]
              removed:
                - root['items']
"""

import logging
import re

from fn import _
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from typing import Optional, List

from jumeaux.addons.judgement import JudgementExecutor
from jumeaux.models import JudgementAddOnPayload, DiffKeys

logger = logging.getLogger(__name__)


class Condition(OwlMixin):
    path: Optional[str]
    added: TList[str]
    removed: TList[str]
    changed: TList[str]

    def __init__(self, path: Optional[str]=None, added: Optional[List[str]]=None, removed: Optional[List[str]]=None, changed: Optional[List[str]]=None):
        self.path = path
        self.added = TList(added) if added is not None else TList()
        self.removed = TList(removed) if removed is not None else TList()
        self.changed = TList(changed) if changed is not None else TList()


class Ignore(OwlMixin):
    title: str
    conditions: TList[Condition]
    image: Optional[str]
    link: Optional[str]

    def __init__(self, title: str, conditions: TList[Condition], image: Optional[str]=None, link: Optional[str]=None):
        self.title = title
        self.conditions = Condition.from_dicts(conditions)
        self.image = image
        self.link = link


class Config(OwlMixin):
    ignores: TList[Ignore]

    def __init__(self, ignores):
        self.ignores = Ignore.from_dicts(ignores)


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict):
        self.config = Config.from_dict(config or {})

    def exec(self, payload: JudgementAddOnPayload) -> JudgementAddOnPayload:
        if payload.regard_as_same or payload.diff_keys is None:
            return payload

        def filter_diff_keys(diff_keys: DiffKeys, condition: Condition) -> DiffKeys:
            if condition.path and not re.search(condition.path, payload.path):
                return diff_keys

            return DiffKeys.from_dict({
                "added": diff_keys.added.reject(
                    lambda dk: condition.added.any(lambda ig: re.search(ig, dk))
                ),
                "removed": diff_keys.removed.reject(
                    lambda dk: condition.removed.any(lambda ig: re.search(ig, dk))
                ),
                "changed": diff_keys.changed.reject(
                    lambda dk: condition.changed.any(lambda ig: re.search(ig, dk))
                )
            })

        filtered_diff_keys = self.config.ignores.flat_map(_.conditions).reduce(filter_diff_keys, payload.diff_keys)
        logger.debug('-'*80)
        logger.debug('filter_diff_keys')
        logger.debug('-'*80)
        logger.debug(filtered_diff_keys.to_pretty_json())

        return JudgementAddOnPayload.from_dict({
            "path": payload.path,
            "qs": payload.qs,
            "headers": payload.headers,
            "res_one": payload.res_one,
            "res_other": payload.res_other,
            "diff_keys": payload.diff_keys.to_dict(),
            "regard_as_same": not (filtered_diff_keys.added or filtered_diff_keys.removed or filtered_diff_keys.changed)
        })
