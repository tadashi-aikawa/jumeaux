# -*- coding:utf-8 -*-

"""For example of config
judgement:
  - name: addons.judgement.ignore_property_addon
    config:
      ignores:
        - path:
            pattern: '/route'
            changed:
              - root['items'][0]
              - root['unit']
"""

import re
from typing import Optional, List
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList
from owlmixin.util import O
from modules.models import JudgementAddOnPayload, DiffKeys


class Path(OwlMixin):
    def __init__(self, pattern: str, added: Optional[List[str]]=None, removed: Optional[List[str]]=None, changed: Optional[List[str]]=None):
        self.pattern: str = pattern
        self.added: TList[str] = TList(added) if added is not None else TList()
        self.removed: TList[str] = TList(removed) if removed is not None else TList()
        self.changed: TList[str] = TList(changed) if changed is not None else TList()


class Ignore(OwlMixin):
    def __init__(self, path: dict):
        self.path: Path = Path.from_dict(path)


class Config(OwlMixin):
    def __init__(self, ignores):
        self.ignores: TList[Ignore] = Ignore.from_dicts(ignores)


def exec(payload: JudgementAddOnPayload, config_dict: dict):
    if payload.regard_as_same or payload.diff_keys is None:
        return payload

    config: Config = Config.from_dict(config_dict or {})

    def filter_diff_keys(diff_keys: DiffKeys, ignore: Ignore) -> DiffKeys:
        if not re.search(ignore.path.pattern, payload.path):
            return diff_keys

        return DiffKeys.from_dict({
            "added": payload.diff_keys.added.reject(
                lambda dk: ignore.path.added.any(lambda ig: re.search(ig, dk))
            ),
            "removed": payload.diff_keys.removed.reject(
                lambda dk: ignore.path.removed.any(lambda ig: re.search(ig, dk))
            ),
            "changed": payload.diff_keys.changed.reject(
                lambda dk: ignore.path.changed.any(lambda ig: re.search(ig, dk))
            )
        })

    filtered_diff_keys = config.ignores.reduce(filter_diff_keys, payload.diff_keys)

    return JudgementAddOnPayload.from_dict({
        "path": payload.path,
        "qs": payload.qs,
        "headers": payload.headers,
        "res_one": payload.res_one,
        "res_other": payload.res_other,
        "diff_keys": payload.diff_keys.to_dict(),
        "regard_as_same": not (filtered_diff_keys.added or filtered_diff_keys.removed or filtered_diff_keys.changed)
    })
