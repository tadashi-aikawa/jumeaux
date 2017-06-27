#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import import_module

from jumeaux.models import *


def create_addon(a: Addon):
    return getattr(import_module(a.name), a.cls_name)(a.config.get())


class AddOnExecutor:
    def __init__(self, addons: Addons):
        self.log2reqs = create_addon(addons.log2reqs)
        self.reqs2reqs = addons.reqs2reqs.map(lambda x: create_addon(x)) if addons else TList()
        self.res2dict = addons.res2dict.map(lambda x: create_addon(x)) if addons else TList()
        self.judgement = addons.judgement.map(lambda x: create_addon(x)) if addons else TList()
        self.store_criterion = addons.store_criterion.map(lambda x: create_addon(x)) if addons else TList()
        self.dump = addons.dump.map(lambda x: create_addon(x)) if addons else TList()
        self.did_challenge = addons.did_challenge.map(lambda x: create_addon(x)) if addons else TList()
        self.final = addons.final.map(lambda x: create_addon(x)) if addons else TList()

    def apply_log2reqs(self, payload: Log2ReqsAddOnPayload) -> TList[Request]:
        return self.log2reqs.exec(payload)

    def apply_reqs2reqs(self, payload: Reqs2ReqsAddOnPayload) -> Reqs2ReqsAddOnPayload:
        return self.reqs2reqs.reduce(lambda p, a: a.exec(p), payload)

    def apply_res2dict(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        return self.res2dict.reduce(lambda p, a: a.exec(p), payload)

    def apply_judgement(self, payload: JudgementAddOnPayload) -> JudgementAddOnPayload:
        return self.judgement.reduce(lambda p, a: a.exec(p), payload)

    def apply_store_criterion(self, payload: StoreCriterionAddOnPayload) -> StoreCriterionAddOnPayload:
        return self.store_criterion.reduce(lambda p, a: a.exec(p), payload)

    def apply_dump(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        return self.dump.reduce(lambda p, a: a.exec(p), payload)

    def apply_did_challenge(self, payload: DidChallengeAddOnPayload) -> DidChallengeAddOnPayload:
        return self.did_challenge.reduce(lambda p, a: a.exec(p), payload)

    def apply_final(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        return self.final.reduce(lambda p, a: a.exec(p), payload)
