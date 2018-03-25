#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import List

from owlmixin import TList, TOption
from owlmixin.util import load_yamlf

from jumeaux.models import Config, Report


def apply_include(addon: dict, config_path: str) -> dict:
    return load_yamlf(os.path.join(os.path.dirname(config_path), addon['include']), 'utf8') \
        if 'include' in addon else addon


def apply_include_addons(addons: dict, config_path: str) -> dict:
    def apply_includes(layer_name: str):
        return [apply_include(a, config_path) for a in addons.get(layer_name, [])]

    return {k: v for k, v in {
        "log2reqs": apply_include(addons["log2reqs"], config_path)
            if "log2reqs" in addons else None,
        "reqs2reqs": apply_includes("reqs2reqs"),
        "res2res": apply_includes("res2res"),
        "res2dict": apply_includes("res2dict"),
        "judgement": apply_includes("judgement"),
        "store_criterion": apply_includes("store_criterion"),
        "dump": apply_includes("dump"),
        "did_challenge": apply_includes("did_challenge"),
        "final": apply_includes("final"),
    }.items() if v}


def create_config(config_paths: TList[str], skip_tags: TOption[TList[str]]) -> Config:
    def filter_by_tags(addons: List[dict]) -> List[dict]:
        return [x for x in addons if skip_tags.map(lambda y: not y.intersection(x.get('tags', []))).get_or(True)]

    def reducer(merged: dict, config_path: str) -> dict:
        d = load_yamlf(config_path, 'utf8')
        if 'addons' in d:
            addons_by_key: dict = d['addons']
            d['addons'] = {k: v for k, v in {
                "log2reqs": addons_by_key.get("log2reqs"),
                "reqs2reqs": filter_by_tags(addons_by_key.get("reqs2reqs", [])),
                "res2res": filter_by_tags(addons_by_key.get("res2res", [])),
                "res2dict": filter_by_tags(addons_by_key.get("res2dict", [])),
                "judgement": filter_by_tags(addons_by_key.get("judgement", [])),
                "store_criterion": filter_by_tags(addons_by_key.get("store_criterion", [])),
                "dump": filter_by_tags(addons_by_key.get("dump", [])),
                "did_challenge": filter_by_tags(addons_by_key.get("did_challenge", [])),
                "final": filter_by_tags(addons_by_key.get("final", [])),
            }.items() if v}
            if 'addons' in merged:
                merged['addons'].update(d['addons'])
                del d['addons']

        merged.update(d)

        if 'addons' in merged:
            merged['addons'].update(apply_include_addons(merged["addons"], config_path))

        return merged

    return Config.from_dict(config_paths.reduce(reducer, {}))


def create_config_from_report(report: Report) -> Config:
    return Config.from_dict({
        "one": report.summary.one.to_dict(),
        "other": report.summary.other.to_dict(),
        "output": report.summary.output.to_dict(),
        "threads": 1,
        "title": report.title,
        "description": report.description,
        "addons": report.addons.get().to_dict()
    })

