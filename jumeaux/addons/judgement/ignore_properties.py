# -*- coding:utf-8 -*-

"""For example of config
judgement:
  - name: jumeaux.addons.judgement.ignore_properties
    config:
      ignores:
        - path:
            pattern: '/route'
            changed:
              - pattern: root['items'][0]
                note: reason
              - root['unit']
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


class RegMatcher(OwlMixin):
    pattern: Optional[str]
    note: Optional[str]
    image: Optional[str]
    link: Optional[str]

    def __init__(self, pattern: Optional[str]=None, note: Optional[str]=None,
                 image: Optional[str]=None, link: Optional[str]=None):
        self.pattern = pattern
        self.note = note
        self.image = image
        self.link = link


class Path(OwlMixin):
    pattern: str
    added: TList[RegMatcher]
    removed: TList[RegMatcher]
    changed: TList[RegMatcher]

    def __init__(self, pattern: str, added: Optional[List[str]]=None, removed: Optional[List[str]]=None, changed: Optional[List[str]]=None):
        self.pattern = pattern
        self.added = RegMatcher.from_optional_dicts(added) if added is not None else TList()
        self.removed = RegMatcher.from_optional_dicts(removed) if removed is not None else TList()
        self.changed = RegMatcher.from_optional_dicts(changed) if changed is not None else TList()


class Ignore(OwlMixin):
    path: Path

    def __init__(self, path: dict):
        self.path = Path.from_dict(path)


class Config(OwlMixin):
    ignores: TList[Ignore]

    def __init__(self, ignores):
        self.ignores = Ignore.from_dicts(ignores)


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict):
        self.config = Config.from_dict(config or {})

    def exec(self, payload: JudgementAddOnPayload):
        if payload.regard_as_same or payload.diff_keys is None:
            return payload

        def filter_diff_keys(diff_keys: DiffKeys, ignore: Ignore) -> DiffKeys:
            if not re.search(ignore.path.pattern, payload.path):
                return diff_keys

            return DiffKeys.from_dict({
                "added": payload.diff_keys.added.reject(
                    lambda dk: ignore.path.added.map(_.pattern).any(lambda ig: re.search(ig, dk))
                ),
                "removed": payload.diff_keys.removed.reject(
                    lambda dk: ignore.path.removed.map(_.pattern).any(lambda ig: re.search(ig, dk))
                ),
                "changed": payload.diff_keys.changed.reject(
                    lambda dk: ignore.path.changed.map(_.pattern).any(lambda ig: re.search(ig, dk))
                )
            })

        filtered_diff_keys = self.config.ignores.reduce(filter_diff_keys, payload.diff_keys)

        return JudgementAddOnPayload.from_dict({
            "path": payload.path,
            "qs": payload.qs,
            "headers": payload.headers,
            "res_one": payload.res_one,
            "res_other": payload.res_other,
            "diff_keys": payload.diff_keys.to_dict(),
            "regard_as_same": not (filtered_diff_keys.added or filtered_diff_keys.removed or filtered_diff_keys.changed)
        })
