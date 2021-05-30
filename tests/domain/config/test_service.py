#!/usr/bin/env python
# -*- coding:utf-8 -*-
# pylint: disable=no-self-use
from owlmixin import TList, TOption

from jumeaux.domain.config import service
from jumeaux.domain.config.vo import Config, MergedArgs


class TestMergeArgs2Config:
    def test_full_args(self):
        args: MergedArgs = MergedArgs.from_dict(
            {
                "files": ["file1", "file2"],
                "title": "test_full_args",
                "description": "Description for test_full_args",
                "tag": ["tag1", "tag2"],
                "threads": 3,
                "processes": 2,
                "max_retries": 5,
            }
        )

        config: Config = Config.from_dict(
            {
                "title": "Config title",
                "description": "Config description",
                "tags": ["tag3", "tag4"],
                "threads": 1,
                "processes": 4,
                "max_retries": 7,
                "judge_response_header": True,
                "one": {
                    "name": "name_one",
                    "host": "http://host/one",
                    "proxy": "http://proxy-one",
                    "headers": {"XXX": "xxx"},
                    "default_response_encoding": "euc-jp",
                },
                "other": {
                    "name": "name_other",
                    "host": "http://host/other",
                    "proxy": "http://proxy-other",
                    "headers": {"YYY": "yyy"},
                    "default_response_encoding": "euc-jp",
                },
                "output": {"encoding": "utf8", "response_dir": "tmpdir"},
                "addons": {
                    "log2reqs": {"name": "addons.log2reqs.csv", "config": {"encoding": "utf8"}}
                },
            }
        )

        assert service.merge_args2config(args, config).to_dict() == {
            "title": "test_full_args",
            "description": "Description for test_full_args",
            "tags": ["tag1", "tag2"],
            "threads": 3,
            "processes": 2,
            "max_retries": 5,
            "judge_response_header": True,
            "input_files": ["file1", "file2"],
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy-one",
                "default_response_encoding": "euc-jp",
                "headers": {"XXX": "xxx"},
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other",
                "proxy": "http://proxy-other",
                "default_response_encoding": "euc-jp",
                "headers": {"YYY": "yyy"},
            },
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
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

    def test_empty_args(self):
        args: MergedArgs = MergedArgs.from_dict({})

        config: Config = Config.from_dict(
            {
                "title": "Config title",
                "description": "Config description",
                "tags": ["tag3", "tag4"],
                "threads": 1,
                "processes": 4,
                "max_retries": 5,
                "judge_response_header": True,
                "one": {"name": "name_one", "host": "http://host/one", "headers": {"XXX": "xxx"}},
                "other": {
                    "name": "name_other",
                    "host": "http://host/other",
                    "headers": {"YYY": "yyy"},
                },
                "output": {"encoding": "utf8", "response_dir": "tmpdir"},
                "addons": {
                    "log2reqs": {"name": "addons.log2reqs.csv", "config": {"encoding": "utf8"}}
                },
            }
        )

        assert service.merge_args2config(args, config).to_dict() == {
            "title": "Config title",
            "description": "Config description",
            "tags": ["tag3", "tag4"],
            "threads": 1,
            "processes": 4,
            "max_retries": 5,
            "judge_response_header": True,
            "one": {"name": "name_one", "host": "http://host/one", "headers": {"XXX": "xxx"}},
            "other": {"name": "name_other", "host": "http://host/other", "headers": {"YYY": "yyy"}},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
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

    def test_empty_args_and_config(self):
        args: MergedArgs = MergedArgs.from_dict({})

        config: Config = Config.from_dict(
            {
                "one": {"name": "name_one", "host": "http://host/one", "headers": {"XXX": "xxx"}},
                "other": {
                    "name": "name_other",
                    "host": "http://host/other",
                    "headers": {"YYY": "yyy"},
                },
                "output": {"encoding": "utf8", "response_dir": "tmpdir"},
                "addons": {
                    "log2reqs": {"name": "addons.log2reqs.csv", "config": {"encoding": "utf8"}}
                },
            }
        )

        assert service.merge_args2config(args, config).to_dict() == {
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
            "one": {"name": "name_one", "host": "http://host/one", "headers": {"XXX": "xxx"}},
            "other": {"name": "name_other", "host": "http://host/other", "headers": {"YYY": "yyy"}},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
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


class TestCreateConfig:
    def test(self, config_only_access_points, config_without_access_points):
        actual: Config = service.create_config(
            TList([config_only_access_points, config_without_access_points]), TOption(None)
        )
        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 3,
            "max_retries": 2,
            "judge_response_header": False,
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
        actual: Config = service.create_config(TList([config_minimum]), TOption(None))

        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
        actual: Config = service.create_config(
            TList([config_with_tags]), TOption(TList(["skip", "skip2"]))
        )

        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "tmpdir"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
        actual: Config = service.create_config(
            TList([config_only_access_points, config_mergecase_1, config_mergecase_2]),
            TOption(None),
        )

        expected = {
            "title": "mergecase_2",
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "mergecase2"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
        actual: Config = service.create_config(
            TList([config_only_access_points, config_mergecase_2, config_mergecase_1]),
            TOption(None),
        )

        expected = {
            "title": "mergecase_2",
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "mergecase1"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
        actual: Config = service.create_config(
            TList([config_with_tags, config_mergecase_with_tags]), TOption(TList(["skip"]))
        )

        expected = {
            "title": "mergecase_with_tags",
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "mergecase_with_tags"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
        actual: Config = service.create_config(
            TList([config_only_access_points, config_includecase_1]), TOption(None)
        )

        expected = {
            "title": "includecase_1",
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy",
                "headers": {},
            },
            "other": {"name": "name_other", "host": "http://host/other", "headers": {}},
            "output": {"encoding": "utf8", "response_dir": "includecase1"},
            "threads": 1,
            "max_retries": 3,
            "judge_response_header": False,
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
