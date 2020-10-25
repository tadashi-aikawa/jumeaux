#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import subprocess

import pytest

import jumeaux.addons  # XXX: Workaround for cyclic import
from jumeaux.models import Report, HttpMethod


def jumeaux(*args) -> int:
    return subprocess.run(["python", "jumeaux/main.py", *args]).returncode


def assert_exists(*paths: str):
    for p in paths:
        assert len(glob.glob(p)) > 0


def assert_exists_in_latest(*paths: str):
    for p in paths:
        assert len(glob.glob(os.path.join("responses/latest", p))) > 0


def assert_not_exists(*paths: str):
    for p in paths:
        assert len(glob.glob(p)) == 0


def load_latest_report() -> Report:
    return Report.from_jsonf("responses/latest/report.json")


class TestHelp:
    def test_usage(self):
        assert jumeaux("-h") == 0


pytestmark = pytest.mark.usefixtures("boot_server", "clean_ws")


class TestInit:
    def test_with_no_args(self):
        assert jumeaux("init") == 1
        assert_not_exists("api", "requests", "config.yml")

    def test_with_invalid_args(self):
        assert jumeaux("init", "hogehoge") == 1
        assert_not_exists("api", "requests", "config.yml")

    def test_simple(self):
        assert jumeaux("init", "simple") == 0
        assert_exists("api", "requests", "config.yml")


class TestRun:
    def test_simple(self):
        assert jumeaux("init", "simple") == 0
        assert jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html",
        )

        report = load_latest_report()
        assert report.summary.status.same == 1
        assert report.summary.status.different == 1
        assert report.trials[0].method == HttpMethod.GET
        assert report.notifiers.is_none()

    def test_post(self):
        assert jumeaux("init", "post") == 0
        assert jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "report.json", "index.html",
        )

        report = load_latest_report()
        assert report.summary.status.same == 1
        assert report.summary.status.different == 2

        assert report.trials[0].method == HttpMethod.POST
        assert report.trials[0].raw.is_none()
        assert report.trials[0].form.get() == {"formparam": ["p11", "p12"]}
        assert report.trials[0].json.is_none()

        assert report.trials[1].method == HttpMethod.POST
        assert report.trials[1].raw.is_none()
        assert report.trials[1].form.is_none()
        assert report.trials[1].json.get() == {
            "id": 1,
            "name": "Ichiro",
        }

        assert report.trials[2].method == HttpMethod.POST
        assert report.trials[2].raw.get() == "a=100&b=200"
        assert report.trials[2].form.is_none()
        assert report.trials[2].json.is_none()
