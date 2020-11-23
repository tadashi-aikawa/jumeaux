#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import shutil
import subprocess

import pytest

import jumeaux.addons  # XXX: Workaround for cyclic import
from jumeaux.domain.config.vo import NotifierType
from jumeaux.models import Report, HttpMethod

URL_BASE = "http://localhost:8000/api"

exec_all = True
is_windows = os.name == "nt"


def cmd_jumeaux(*args: str) -> int:
    return subprocess.run(["python", "jumeaux/main.py", *args]).returncode


def assert_exists(*paths: str):
    for p in paths:
        assert len(glob.glob(p)) > 0


def assert_exists_in_latest(*paths: str):
    for p in paths:
        assert_exists(os.path.join("responses/latest", p))


def assert_not_exists(*paths: str):
    for p in paths:
        assert len(glob.glob(p)) == 0


def assert_not_exists_in_latest(*paths: str):
    for p in paths:
        assert_not_exists(os.path.join("responses/latest", p))


def ls_recursively(path: str, depth: int = 0):
    for e in os.listdir(path):
        if os.path.isdir(f"{path}/{e}"):
            print(f" {'  ' * depth}∟📂 {e}")
            ls_recursively(f"{path}/{e}", depth + 1)
        else:
            print(f" {'  ' * depth}∟📄 {e}")


def load_latest_report() -> Report:
    r = Report.from_jsonf("responses/latest/report.json")

    print(
        f"""
------------------------------
| 📄 report.json
------------------------------
{r.to_pretty_json()}

------------------------------
| 📂 responses/latest
------------------------------ """
    )
    ls_recursively("responses/latest", 1)

    return r


class TestHelp:
    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_usage(self):
        assert cmd_jumeaux("-h") == 0


@pytest.mark.usefixtures("clean_ws")
class TestInit:
    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_no_args(self):
        assert cmd_jumeaux("init") == 1
        assert_not_exists("api", "requests", "config.yml")

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_invalid_args(self):
        assert cmd_jumeaux("init", "hogehoge") == 1
        assert_not_exists("api", "requests", "config.yml")

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_simple(self):
        assert cmd_jumeaux("init", "simple") == 0
        assert_exists("api", "requests", "config.yml")


@pytest.mark.usefixtures("clean_ws", "boot_server")
class TestRun:
    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_simple(self):
        assert cmd_jumeaux("init", "simple") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html",
        )

        report = load_latest_report()

        assert report.summary.status.same == 1
        assert report.summary.status.different == 1

        assert report.trials[0].method == HttpMethod.GET

        assert report.notifiers.is_none()

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_path_custom(self):
        assert cmd_jumeaux("init", "path_custom") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "other-props/*", "report.json", "index.html",
        )

        report = load_latest_report()

        assert report.summary.status.same == 0
        assert report.summary.status.different == 2
        assert report.summary.one.path.get().before == "json"
        assert report.summary.one.path.get().after == "xml"
        assert report.summary.other.path.get().before == r"([^-]+)-(\d).json"
        assert report.summary.other.path.get().after == r"\1/case-\2.json"

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_query_custom(self):
        assert cmd_jumeaux("init", "query_custom") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html",
        )

        report = load_latest_report()

        assert report.summary.status.same == 1
        assert report.summary.status.different == 1
        assert report.summary.one.query.is_none()
        assert report.summary.other.query.get().overwrite.get()["additional"][0] == "hoge"
        assert report.summary.other.query.get().remove.get()[0] == "param"

        assert report.trials[0].one.url == f"{URL_BASE}/one/same-1.json"
        assert report.trials[0].other.url == f"{URL_BASE}/other/same-1.json?additional=hoge"

        assert report.trials[1].one.url == f"{URL_BASE}/one/diff-1.json?param=123"
        assert report.trials[1].other.url == f"{URL_BASE}/other/diff-1.json?additional=hoge"

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_all_same(self):
        assert cmd_jumeaux("init", "all_same") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest("report.json", "index.html")
        assert_not_exists_in_latest("one/*", "other/*", "one-props/*", "other-props/*")

        report = load_latest_report()

        assert report.summary.status.same == 1
        assert report.summary.status.different == 0

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_xml(self):
        assert cmd_jumeaux("init", "xml") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.status.same == 0
        assert report.summary.status.different == 1
        assert report.trials[0].tags == ["over $10 (id=bk101)"]

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_html(self):
        assert cmd_jumeaux("init", "html") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.status.same == 0
        assert report.summary.status.different == 1

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_ignore_order(self):
        assert cmd_jumeaux("init", "ignore_order") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.status.same == 1
        assert report.summary.status.different == 2

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_ignore(self):
        assert cmd_jumeaux("init", "ignore") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.status.same == 2
        assert report.summary.status.different == 1

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_force_json(self):
        assert cmd_jumeaux("init", "force_json") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.trials[0].one.type == "plain"
        assert report.trials[0].other.type == "plain"
        assert report.trials[1].one.type == "json"
        assert report.trials[1].other.type == "json"

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_request_headers(self):
        assert cmd_jumeaux("init", "request_headers") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.one.headers["XXX-Header-Key"] == "xxx-header-key-one"
        assert report.summary.one.headers["User-Agent"] == "jumeaux-test"
        assert report.summary.other.headers["XXX-Header-Key"] == "xxx-header-key-other"

        assert report.trials[0].headers == {}
        assert report.trials[1].headers["User-Agent"] == "Hack by requests!"
        assert report.trials[2].headers == {}
        assert report.trials[3].headers["User-Agent"] == "Hack by requests!"

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_log_level_options(self):
        assert cmd_jumeaux("init", "simple") == 0
        assert cmd_jumeaux("run", "requests", "-v") == 0
        assert cmd_jumeaux("run", "requests", "-vv") == 0
        assert cmd_jumeaux("run", "requests", "-vvv") == 0

        assert_exists("responses")

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_threads(self):
        assert cmd_jumeaux("init", "simple") == 0
        assert cmd_jumeaux("run", "requests", "--threads", "2") == 0

        assert_exists("responses")

        report = load_latest_report()

        assert report.summary.concurrency.threads == 2
        assert report.summary.concurrency.processes == 1

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    @pytest.mark.skipif(
        is_windows, reason="Jumeaux doesn't support multiprocess executor in Windows."
    )
    def test_with_processes(self):
        assert cmd_jumeaux("init", "simple") == 0
        assert cmd_jumeaux("run", "requests", "--processes", "2") == 0

        assert_exists("responses")

        report = load_latest_report()

        assert report.summary.concurrency.threads == 1
        assert report.summary.concurrency.processes == 2

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_root_array(self):
        assert cmd_jumeaux("init", "root_array") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.summary.status.same == 1
        assert report.summary.status.different == 1

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_notifier(self):
        assert cmd_jumeaux("init", "notifier") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "other-props/*", "report.json", "index.html"
        )

        report = load_latest_report()

        assert report.notifiers.get().get("jumeaux").get().type == NotifierType.SLACK
        assert report.notifiers.get().get("jumeaux").get().channel.get() == "#bot_tadashi-aikawa"
        assert report.notifiers.get().get("jumeaux").get().icon_emoji.get() == "miroir"

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_post(self):
        assert cmd_jumeaux("init", "post") == 0
        assert cmd_jumeaux("run", "requests") == 0
        assert_exists_in_latest(
            "one/*", "other/*", "one-props/*", "report.json", "index.html",
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


@pytest.mark.usefixtures("clean_ws", "boot_server")
class TestRetry:
    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_empty_path(self):
        assert cmd_jumeaux("init", "path_empty") == 0
        assert cmd_jumeaux("run", "requests") == 0

        shutil.move("responses/latest/report.json", "report.json")

        assert cmd_jumeaux("retry", "report.json") == 0
        os.remove("report.json")

        report = load_latest_report()

        assert_exists_in_latest("report.json", "index.html")

        assert report.summary.status.same == 0
        assert report.summary.status.different == 1

    @pytest.mark.skipif(exec_all is False, reason="Need not exec all test")
    def test_with_notifiers(self):
        assert cmd_jumeaux("init", "notifier") == 0
        assert cmd_jumeaux("run", "requests") == 0

        shutil.move("responses/latest/report.json", "report.json")

        assert cmd_jumeaux("retry", "report.json") == 0
        os.remove("report.json")

        report = load_latest_report()

        assert_exists_in_latest("report.json", "index.html")

        assert report.notifiers.get().get("jumeaux").get().type == NotifierType.SLACK
        assert report.notifiers.get().get("jumeaux").get().channel.get() == "#bot_tadashi-aikawa"
        assert report.notifiers.get().get("jumeaux").get().icon_emoji.get() == "miroir"
