# -*- coding: utf-8 -*-
from owlmixin import OwlMixin, TOption, TList


class Addon(OwlMixin):
    name: str
    cls_name: str = "Executor"
    config: TOption[dict]
    include: TOption[str]
    tags: TOption[TList[str]]


# List is None...
class Addons(OwlMixin):
    log2reqs: Addon
    reqs2reqs: TList[Addon] = []
    res2res: TList[Addon] = []
    res2dict: TList[Addon] = []
    judgement: TList[Addon] = []
    store_criterion: TList[Addon] = []
    dump: TList[Addon] = []
    did_challenge: TList[Addon] = []
    final: TList[Addon] = []
