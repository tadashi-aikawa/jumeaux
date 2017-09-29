#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with open(os.path.join(here, 'README.rst')) as f:
        return f.read()


def load_required_modules():
    with open(os.path.join(here, "requirements.txt")) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


setup(
    name='jumeaux',
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open('jumeaux/__init__.py').read()).group(1),
    description='Check difference between two responses of API.',
    long_description=load_readme(),
    license='MIT',
    author='tadashi-aikawa',
    author_email='syou.maman@gmail.com',
    maintainer='tadashi-aikawa',
    maintainer_email='syou.maman@gmail.com',
    url='https://github.com/tadashi-aikawa/jumeaux.git',
    keywords='diff rest api response two one other',
    packages=find_packages(exclude=['tests*']),
    install_requires=load_required_modules(),
    extras_require={
        'test': ['pytest', 'pytest-cov'],
        'doc': ['mkdocs', 'mkdocs-material', 'pymdown-extensions', 'fontawesome-markdown'],
    },
    entry_points={
        'console_scripts': [
            'jumeaux = jumeaux.executor:main'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
)
