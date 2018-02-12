#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with open(os.path.join(here, 'README.rst')) as f:
        return f.read()


setup(
    name='addon_sample',
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open('addon_sample/__init__.py').read()).group(1),
    packages=find_packages(exclude=['tests*'])
)
