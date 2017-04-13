#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.models import *
from importlib import import_module
from fn import _
from owlmixin.util import O


def create_addon(a: Addon):
    return getattr(import_module(a.name), a.command)(a.config)


class AddOnExecutor:
    def __init__(self, addons: Addons):
        self.log = create_addon(addons.log)
        self.res2dict = O(addons).then(_.res2dict).or_(TList()).map(lambda x: create_addon(x))
        self.dump = O(addons).then(_.dump).or_(TList()).map(lambda x: create_addon(x))
        self.after = O(addons).then(_.after).or_(TList()).map(lambda x: create_addon(x))
        self.request = O(addons).then(_.request).or_(TList()).map(lambda x: create_addon(x))
        self.judgement = O(addons).then(_.judgement).or_(TList()).map(lambda x: create_addon(x))

    def apply_log(self, payload: LogAddOnPayload) -> TList[Request]:
        return self.log.exec(payload)

    def apply_res2dict(self, payload: Res2DictAddOnPayload) -> Res2DictAddOnPayload:
        return self.res2dict.reduce(lambda p, a: a.exec(p), payload)

    def apply_dump(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        return self.dump.reduce(lambda p, a: a.exec(p), payload)

    def apply_after(self, payload: AfterAddOnPayload) -> AfterAddOnPayload:
        return self.after.reduce(lambda p, a: a.exec(p), payload)

    def apply_request(self, payload: RequestAddOnPayload) -> RequestAddOnPayload:
        return self.request.reduce(lambda p, a: a.exec(p), payload)

    def apply_judgement(self, payload: JudgementAddOnPayload) -> JudgementAddOnPayload:
        return self.judgement.reduce(lambda p, a: a.exec(p), payload)
