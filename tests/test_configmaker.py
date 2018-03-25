#!/usr/bin/env python
# -*- coding:utf-8 -*-

from owlmixin import TList

from jumeaux import configmaker
from jumeaux.models import Config


class TestCreateConfig:
    def test(self, config_only_access_points, config_without_access_points):
        actual: Config = configmaker.create_config(TList([config_only_access_points, config_without_access_points]), ['TODO'])
        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "tmpdir"
            },
            "threads": 3,
            "max_retries": 2,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

    def test_no_base(self, config_minimum):
        actual: Config = configmaker.create_config(TList([config_minimum]), ['TODO'])

        expected = {
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "tmpdir"
            },
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [
                    {
                        "name": "addons.store_criterion.general",
                        "cls_name": "Executor",
                        "config": {
                            "statuses": [
                                "different"
                            ]
                        }
                    }
                ],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

    def test_mergecase1then2(self, config_only_access_points, config_mergecase_1, config_mergecase_2):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_mergecase_1, config_mergecase_2]), ['TODO'])

        expected = {
            "title": 'mergecase_2',
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "mergecase2"
            },
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.random",
                        "cls_name": "Executor"
                    }
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

    def test_mergecase2then1(self, config_only_access_points, config_mergecase_1, config_mergecase_2):
        actual: Config = configmaker.create_config(
            TList([config_only_access_points, config_mergecase_2, config_mergecase_1]), ['TODO'])

        expected = {
            "title": 'mergecase_2',
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "mergecase1"
            },
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {
                            "size": 5
                        }
                    }
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

    def test_includecase1(self, config_only_access_points, config_includecase_1):
        actual: Config = configmaker.create_config(TList([config_only_access_points, config_includecase_1]), ['TODO'])

        expected = {
            "title": 'includecase_1',
            "one": {
                "name": "name_one",
                "host": "http://host/one",
                "proxy": "http://proxy"
            },
            "other": {
                "name": "name_other",
                "host": "http://host/other"
            },
            "output": {
                "encoding": "utf8",
                "response_dir": "includecase1"
            },
            "threads": 1,
            "max_retries": 3,
            "addons": {
                "log2reqs": {
                    "name": "addons.log2reqs.csv",
                    "cls_name": "Executor",
                    "config": {
                        "encoding": "utf8"
                    }
                },
                "reqs2reqs": [
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {
                            "size": 999
                        }
                    },
                    {
                        "name": "addons.reqs2reqs.head",
                        "cls_name": "Executor",
                        "config": {
                            "size": 5
                        }
                    }
                ],
                "res2res": [],
                "res2dict": [],
                "judgement": [],
                "store_criterion": [],
                "dump": [],
                "did_challenge": [],
                "final": []
            }
        }

        assert actual.to_dict() == expected

