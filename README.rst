Jumeaux
*******

|travis| |coverage| |complexity| |license|

Check difference between two responses of API.

Outline
=======

.. contents::


Features
========

todo


Requirement
===========

* Python3.6 and uppper


Installation
============

.. sourcecode:: bash

    $ pip install jumeaux
    $ jumeaux --version
    0.5.0


Run
===

For example

.. sourcecode:: bash

    $ jumeaux --config sample/config.yaml sample/requests.csv

It is case if you don't want to specify input logs. This is same as above because `config.yaml` can specify input files.

.. sourcecode:: bash

    $ jumeaux --config sample/config.yaml


Then you can see

* API responses in `response/d986a822e0dfab08bfdf833094817b40995653734f2086e304a9af6723fcb124`
* INFO logs and report(json) as following

.. sourcecode::

    INFO Challenge:  1 / 3 -- README
    INFO Request one:   https://api.github.com/repos/tadashi-aikawa/jumeaux/readme?
    INFO Request other: https://api.github.com/repos/tadashi-aikawa/owlmixin/readme?
    INFO Response one:   200 / 1.33s / 2843b / application/json; charset=utf-8
    INFO Response other: 200 / 1.33s / 8814b / application/json; charset=utf-8
    INFO Status:   different
    INFO Challenge:  2 / 3 -- commit
    INFO Request one:   https://api.github.com/repos/tadashi-aikawa/jumeaux/commits?path=README.md
    INFO Request other: https://api.github.com/repos/tadashi-aikawa/owlmixin/commits?path=README.md
    INFO Response one:   200 / 1.02s / 4083b / application/json; charset=utf-8
    INFO Response other: 200 / 1.02s / 43634b / application/json; charset=utf-8
    INFO Status:   different
    INFO Challenge:  3 / 3 -- wrong path
    INFO Request one:   https://api.github.com/repos/tadashi-aikawa/jumeaux/hogehoge?
    INFO Request other: https://api.github.com/repos/tadashi-aikawa/owlmixin/hogehoge?
    INFO Response one:   404 / 0.97s / 77b / application/json; charset=utf-8
    INFO Response other: 404 / 0.96s / 77b / application/json; charset=utf-8
    INFO Status:   same
    {
        "key": "d986a822e0dfab08bfdf833094817b40995653734f2086e304a9af6723fcb124",
        "title": "DEMO",
        "summary": {
            "one": {
                "host": "https://api.github.com/repos/tadashi-aikawa/jumeaux",
                "name": "jumeaux"
            },
            "other": {
                "host": "https://api.github.com/repos/tadashi-aikawa/owlmixin",
                "name": "owlmixin"
            },
            "output": {
                "encoding": "utf8",
                "logger": {
                    "disable_existing_loggers": false,
                    "formatters": {
                        "simple": {
                            "format": "%(levelname)s %(message)s"
                        }
                    },
                    "handlers": {
                        "console": {
                            "class": "logging.StreamHandler",
                            "formatter": "simple",
                            "level": "INFO",
                            "stream": "ext://sys.stderr"
                        }
                    },
                    "root": {
                        "handlers": [
                            "console"
                        ],
                        "level": "INFO"
                    },
                    "version": 1
                },
                "response_dir": "response"
            },
            "paths": {
                "/commits": 1,
                "/hogehoge": 1,
                "/readme": 1
            },
            "status": {
                "different": 2,
                "failure": 0,
                "same": 1
            },
            "time": {
                "elapsed_sec": 3,
                "end": "2017/04/28 23:35:50",
                "start": "2017/04/28 23:35:46"
            }
        },
        "addons": {
            "dump": [
                {
                    "cls_name": "Executor",
                    "name": "jumeaux.addons.dump.json"
                }
            ],
            "final": [],
            "judgement": [],
            "log2reqs": {
                "cls_name": "Executor",
                "config": {
                    "encoding": "utf8"
                },
                "name": "jumeaux.addons.log2reqs.csv"
            },
            "reqs2reqs": [],
            "res2dict": []
        },
        "trials": [
            {
                "headers": {},
                "name": "README",
                "one": {
                    "byte": 2843,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "file": "one/(1)README",
                    "response_sec": 1.33,
                    "status_code": 200,
                    "url": "https://api.github.com/repos/tadashi-aikawa/jumeaux/readme"
                },
                "other": {
                    "byte": 8814,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "file": "other/(1)README",
                    "response_sec": 1.33,
                    "status_code": 200,
                    "url": "https://api.github.com/repos/tadashi-aikawa/owlmixin/readme"
                },
                "path": "/readme",
                "queries": {},
                "request_time": "2017/04/28 23:35:46",
                "seq": 1,
                "status": "different"
            },
            {
                "headers": {},
                "name": "commit",
                "one": {
                    "byte": 4083,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "file": "one/(2)commit",
                    "response_sec": 1.02,
                    "status_code": 200,
                    "url": "https://api.github.com/repos/tadashi-aikawa/jumeaux/commits?path=README.md"
                },
                "other": {
                    "byte": 43634,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "file": "other/(2)commit",
                    "response_sec": 1.02,
                    "status_code": 200,
                    "url": "https://api.github.com/repos/tadashi-aikawa/owlmixin/commits?path=README.md"
                },
                "path": "/commits",
                "queries": {
                    "path": [
                        "README.md"
                    ]
                },
                "request_time": "2017/04/28 23:35:48",
                "seq": 2,
                "status": "different"
            },
            {
                "headers": {},
                "name": "wrong path",
                "one": {
                    "byte": 77,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "response_sec": 0.97,
                    "status_code": 404,
                    "url": "https://api.github.com/repos/tadashi-aikawa/jumeaux/hogehoge"
                },
                "other": {
                    "byte": 77,
                    "content_type": "application/json; charset=utf-8",
                    "encoding": "utf-8",
                    "response_sec": 0.96,
                    "status_code": 404,
                    "url": "https://api.github.com/repos/tadashi-aikawa/owlmixin/hogehoge"
                },
                "path": "/hogehoge",
                "queries": {},
                "request_time": "2017/04/28 23:35:49",
                "seq": 3,
                "status": "same"
            }
        ]
    }




Test Result
===========

Master
------

.. image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux

Current
-------

.. image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux


Licence
=======

MIT
---

This software is released under the MIT License, see LICENSE.txt.


.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.svg?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux/builds
    :alt: Build Status
.. |coverage| image:: https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/coverage.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/jumeaux/coverage
    :alt: Test Coverage
.. |complexity| image:: https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/gpa.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/jumeaux
    :alt: Code Climate
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
