#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

REQUIRES = [
    "requests",
    "docopt",
    "schema",
    "xmltodict",
    "fn",
    "boto3",
    "freezegun",
    "pydash",
    "requests-toolbelt",
    "jinja2",
    "beautifulsoup4",
    "lxml",
    "livereload",
    "tzlocal",
    "deepdiff==3.3.0",
    "owlmixin>=4.0.3",
]

DEV_REQUIRES = [
    "pytest",
    "pytest-cov",
    "twine",
    "wheel",
    "mkdocs",
    "mkdocs-material",
    "pymdown-extensions",
    "fontawesome-markdown",
    "pylint",
    "black",
    # sphinx, twine vulnerables
    "urllib3>=1.24.2",
]

here = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with open(os.path.join(here, "README.md")) as f:
        return f.read()


target_files = []
for root, dirs, files in os.walk(f"{here}/jumeaux/sample"):
    targets = [os.path.join(root, f) for f in files]
    target_files.extend(targets)

setup(
    name="jumeaux",
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open("jumeaux/__init__.py").read(),
    ).group(1),
    description="Check difference between two responses of API.",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="tadashi-aikawa",
    author_email="syou.maman@gmail.com",
    maintainer="tadashi-aikawa",
    maintainer_email="syou.maman@gmail.com",
    url="https://github.com/tadashi-aikawa/jumeaux.git",
    keywords="diff rest api response two one other",
    packages=find_packages(exclude=["tests*"]),
    package_data={"jumeaux": target_files},
    install_requires=REQUIRES,
    extras_require={"dev": DEV_REQUIRES},
    entry_points={"console_scripts": ["jumeaux = jumeaux.executor:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
