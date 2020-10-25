#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import subprocess

import pytest


@pytest.fixture()
def clean_ws():
    os.path.exists("api") and shutil.rmtree("api")
    os.path.exists("responses") and shutil.rmtree("responses")
    os.path.exists("requests") and os.remove("requests")
    os.path.exists("config.yml") and os.remove("config.yml")


@pytest.fixture(scope="module")
def boot_server():
    print("boot_server start")
    p = subprocess.Popen(["python", "jumeaux/main.py", "server"])
    yield

    pid = p.pid
    print(f"boot_server returned: {pid}")
    p.kill()
    print(f"boot_server killed: {pid}")
