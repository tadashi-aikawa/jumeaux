#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import subprocess
import sys
import time

import pytest


def clean_workspace():
    print("fixture: clean_ws")
    os.path.exists("api") and shutil.rmtree("api")
    os.path.exists("responses") and shutil.rmtree("responses")
    os.path.exists("requests") and os.remove("requests")
    os.path.exists("config.yml") and os.remove("config.yml")


@pytest.fixture()
def clean_ws():
    clean_workspace()
    yield
    clean_workspace()


@pytest.fixture(scope="module")
def boot_server():
    print("fixture: boot_server start")
    p = subprocess.Popen(
        [
            sys.executable,
            "jumeaux/main.py",
            "server",
        ]
    )
    print("Wait 5 seconds for a server to end booting")
    time.sleep(5)
    yield

    pid = p.pid
    print(f"boot_server returned: {pid}")
    p.kill()
    print(f"boot_server killed: {pid}")
