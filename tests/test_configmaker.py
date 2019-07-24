#!/usr/bin/env python
# -*- coding:utf-8 -*-
# pylint: disable=no-self-use

from owlmixin import TList, TOption

from jumeaux import configmaker
from jumeaux.models import Config


class TestCreateConfig:
    def test(self, config_only_access_points, config_without_access_points):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_without_access_points]), TOption(None)
        )
        expected = {
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 3,
            "max_retries": 2,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_no_base(self, config_minimum):
        actual: Config = configmaker.create_config(TList([config_minimum]), TOption(None))

        expected = {
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [
                    {
                        "name": "addons.store_criterion.free",
                        "cls_name": "Executor",
                        "config": {"when_any": ["status == 'different'"]},
                    }
                ],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_no_base_skip_tags(self, config_with_tags):
        actual: Config = configmaker.create_config(
            TList([config_with_tags]), TOption(TList(["skip", "skip2"]))
        )

        expected = {
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "tags": ["no-skip"],
                        "config": {"size": 1},
                    },
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {"size": 3},
                    },
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_mergecase1then2(
        self, config_only_access_points, config_mergecase_1, config_mergecase_2
    ):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_mergecase_1, config_mergecase_2]),
            TOption(None),
        )

        expected = {
            "title": "mergecase_2",
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "mergecase2"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [{"name": "addons.reqs2reqs.random", "cls_name": "Executor"}],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_mergecase2then1(
        self, config_only_access_points, config_mergecase_1, config_mergecase_2
    ):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_mergecase_2, config_mergecase_1]),
            TOption(None),
        )

        expected = {
            "title": "mergecase_2",
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "mergecase1"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [
                    {"name": "addons.reqs2reqs.head", "cls_name": "Executor", "config": {"size": 5}}
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_mergecase_with_tags(self, config_with_tags, config_mergecase_with_tags):
        actual: Config = configmaker.create_config(
            TList([config_with_tags, config_mergecase_with_tags]), TOption(TList(["skip"]))
        )

        expected = {
            "title": "mergecase_with_tags",
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "mergecase_with_tags"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "tags": ["no-skip"],
                        "config": {"size": 2},
                    }
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [
                    {
                        "name": "addons.store_criterion.free",
                        "cls_name": "Executor",
                        "tags": ["skip2"],
                        "config": {"when_any": ["status == 'different'"]},
                    }
                ],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected

    def test_includecase1(self, config_only_access_points, config_includecase_1):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_includecase_1]), TOption(None)
        )

        expected = {
            "title": "includecase_1",
            "one": {"name": "name_one", "host": "http://host/one", "proxy": "http://proxy"},
            "other": {"name": "name_other", "host": "http://host/other"},
            "output": {"encoding": "utf8", "response_dir": "includecase1"},
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {"encoding": "utf8"},
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {"size": 999},
                    },
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {"size": 5},
                    },
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": [],
            },
        }

        assert actual.to_dict() == expected
