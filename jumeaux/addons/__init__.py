#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fn import _
from importlib import import_module
from owlmixin.util import O

from jumeaux.models import *


def create_addon(a: Addon):
    return getattr(import_module(a.name), a.cls_name)(a.config)


class AddOnExecutor:
    def __init__(self, addons: Addons):
        self.log2reqs = create_addon(addons.log2reqs)
        self.reqs2reqs = O(addons).then(_.reqs2reqs).or_(TList()).map(lambda x: create_addon(x))
        self.res2dict = O(addons).then(_.res2dict).or_(TList()).map(lambda x: create_addon(x))
        self.judgement = O(addons).then(_.judgement).or_(TList()).map(lambda x: create_addon(x))
        self.store_criterion = O(addons).then(_.store_criterion).or_(TList()).map(lambda x: create_addon(x))
        self.dump = O(addons).then(_.dump).or_(TList()).map(lambda x: create_addon(x))
        self.did_challenge = O(addons).then(_.did_challenge).or_(TList()).map(lambda x: create_addon(x))
        self.final = O(addons).then(_.final).or_(TList()).map(lambda x: create_addon(x))

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
