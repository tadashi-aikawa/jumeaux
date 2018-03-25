#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from owlmixin import TList, TOption
from owlmixin.util import load_yamlf

from jumeaux.models import Config, Report


def create_config(config_paths: TList[str], skip_tags: TOption[TList[str]]) -> Config:
    def apply_include(addon: dict, config_path: str) -> dict:
        return load_yamlf(os.path.join(os.path.dirname(config_path), addon['include']), 'utf8') \
            if 'include' in addon else addon

    def apply_include_addons(addons: dict, config_path: str) -> dict:
        def apply_includes(name: str):
            return [apply_include(a, config_path) for a in addons.get(name, [])]

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

    def reducer(merged: dict, config_path: str) -> dict:
        d = load_yamlf(config_path, 'utf8')
        if 'addons' in d and 'addons' in merged:
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

