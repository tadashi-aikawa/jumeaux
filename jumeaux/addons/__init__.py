#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import import_module
from importlib.util import find_spec
from owlmixin import TList

from jumeaux.models import (
    Addon,
    Addons,
    Request,
    Config,
    Log2ReqsAddOnPayload,
    Reqs2ReqsAddOnPayload,
    Res2ResAddOnPayload,
    Res2DictAddOnPayload,
    JudgementAddOnPayload,
    JudgementAddOnReference,
    StoreCriterionAddOnPayload,
    StoreCriterionAddOnReference,
    DidChallengeAddOnPayload,
    DidChallengeAddOnReference,
    DumpAddOnPayload,
    FinalAddOnPayload,
)


def create_addon(a: Addon, layer: str):
    try:
        relative_name = f'{__name__}.{layer}.{a.name}'
        if find_spec(relative_name):
            return getattr(import_module(relative_name), a.cls_name)(a.config.get())
    except ModuleNotFoundError as e:
        pass

    try:
        if find_spec(a.name):
            return getattr(import_module(a.name), a.cls_name)(a.config.get())
    except ModuleNotFoundError as e:
        pass

    raise ModuleNotFoundError(f'''
<< {a.name} >> is invalid add-on name.
Please check either if << {relative_name} >> or << {a.name} >> are exist.
''')


class AddOnExecutor:
    def __init__(self, addons: Addons) -> None:
        self.log2reqs = create_addon(addons.log2reqs, 'log2reqs')
        self.reqs2reqs = addons.reqs2reqs.map(lambda x: create_addon(x, 'reqs2reqs')) if addons else TList()
        self.res2res = addons.res2res.map(lambda x: create_addon(x, 'res2res')) if addons else TList()
        self.res2dict = addons.res2dict.map(lambda x: create_addon(x, 'res2dict')) if addons else TList()
        self.judgement = addons.judgement.map(lambda x: create_addon(x, 'judgement')) if addons else TList()
        self.store_criterion = addons.store_criterion.map(lambda x: create_addon(x, 'store_criterion')) if addons else TList()
        self.dump = addons.dump.map(lambda x: create_addon(x, 'dump')) if addons else TList()
        self.did_challenge = addons.did_challenge.map(lambda x: create_addon(x, 'did_challenge')) if addons else TList()
        self.final = addons.final.map(lambda x: create_addon(x, 'final')) if addons else TList()

    def apply_log2reqs(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        return self.log2reqs.exec(payload)

    def apply_reqs2reqs(self, payload: Reqs2ReqsAddOnPayload, config: Config) -> Reqs2ReqsAddOnPayload:
        return self.reqs2reqs.reduce(lambda p, a: a.exec(p, config), payload)

    def apply_res2res(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        return self.res2res.reduce(lambda p, a: a.exec(p), payload)

    def apply_res2dict(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        return self.res2dict.reduce(lambda p, a: a.exec(p), payload)

    def apply_judgement(self, payload: JudgementAddOnPayload, reference: JudgementAddOnReference) -> JudgementAddOnPayload:
        return self.judgement.reduce(lambda p, a: a.exec(p, reference), payload)

    def apply_store_criterion(self,
                              payload: StoreCriterionAddOnPayload,
                              reference: StoreCriterionAddOnReference) -> StoreCriterionAddOnPayload:
        return self.store_criterion.reduce(lambda p, a: a.exec(p, reference), payload)

    def apply_dump(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        return self.dump.reduce(lambda p, a: a.exec(p), payload)

    def apply_did_challenge(self, payload: DidChallengeAddOnPayload, reference: DidChallengeAddOnReference) -> DidChallengeAddOnPayload:
        return self.did_challenge.reduce(lambda p, a: a.exec(p, reference), payload)

    def apply_final(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        return self.final.reduce(lambda p, a: a.exec(p), payload)
