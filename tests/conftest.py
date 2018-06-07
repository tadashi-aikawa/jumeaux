#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
from typing import Iterator, Callable


@pytest.fixture
def create_tmpfile_from(tmpdir) -> Callable[[str], str]:
    def func(content: str) -> str:
        tmpfile = tmpdir.join('tmpfile')
        with tmpfile.open('w') as f:
            f.write(content)
        return str(tmpfile)

    yield func


@pytest.fixture
def config_minimum(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_minimum.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
one:
  name: name_one
  host: http://host/one
  proxy: http://proxy
other:
  name: name_other
  host: http://host/other
output:
  encoding: utf8
  response_dir: tmpdir
addons:
  log2reqs:
    name: addons.log2reqs.csv
    config:
      encoding: utf8
  store_criterion:
    - name: addons.store_criterion.general
      config:
        statuses:
          - different
        ''')

    yield str(tmpfile)


@pytest.fixture
def config_with_tags(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_with_tags.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
one:
  name: name_one
  host: http://host/one
  proxy: http://proxy
other:
  name: name_other
  host: http://host/other
output:
  encoding: utf8
  response_dir: tmpdir
addons:
  log2reqs:
    name: addons.log2reqs.csv
    config:
      encoding: utf8
  reqs2reqs:
    - name: addons.reqs2reqs.head
      tags: ['no-skip']
      config:
        size: 1
    - name: addons.reqs2reqs.head
      tags: ['skip']
      config:
        size: 2
    - name: addons.reqs2reqs.head
      config:
        size: 3
    - name: addons.reqs2reqs.head
      tags: ['hoge', 'skip2']
      config:
        size: 4
  store_criterion:
    - name: addons.store_criterion.general
      tags: ['skip2']
      config:
        statuses:
          - different
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_without_access_points(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_without_access_points.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
threads: 3
max_retries: 2
output:
  encoding: utf8
  response_dir: tmpdir
addons:
  log2reqs:
    name: addons.log2reqs.csv
    config:
      encoding: utf8
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_only_access_points(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_only_access_points.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
one:
  name: name_one
  host: http://host/one
  proxy: http://proxy
other:
  name: name_other
  host: http://host/other
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_mergecase_1(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_mergecase_1.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
output:
  encoding: utf8
  response_dir: mergecase1
addons:
  log2reqs:
    name: addons.log2reqs.csv
    config:
      encoding: utf8
  reqs2reqs:
    - name: addons.reqs2reqs.head
      config:
        size: 5
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_mergecase_2(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_mergecase_2.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
title: mergecase_2
output:
  encoding: utf8
  response_dir: mergecase2
addons:
  reqs2reqs:
    - name: addons.reqs2reqs.random
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_mergecase_with_tags(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_mergecase_with_tags.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
title: mergecase_with_tags
output:
  encoding: utf8
  response_dir: mergecase_with_tags
addons:
  reqs2reqs:
    - name: addons.reqs2reqs.head
      tags: ['skip']
      config:
        size: 1
    - name: addons.reqs2reqs.head
      tags: ['no-skip']
      config:
        size: 2
        ''')

    yield str(tmpfile)

    tmpfile.remove()


@pytest.fixture
def config_includecase_1(tmpdir) -> Iterator[str]:
    tmpfile = tmpdir.join('config_includecase_1.yml')

    with tmpfile.open('w') as f:
        f.write(f'''
title: includecase_1
output:
  encoding: utf8
  response_dir: includecase1
addons:
  log2reqs:
    name: addons.log2reqs.csv
    config:
      encoding: utf8
  reqs2reqs:
    - include: config_head.yml
    - name: addons.reqs2reqs.head
      config:
        size: 5
        ''')

    tmpfile2 = tmpdir.join('config_head.yml')
    with tmpfile2.open('w') as f:
        f.write(f'''
    name: addons.reqs2reqs.head
    config:
      size: 999
            ''')

    yield str(tmpfile)

    tmpfile.remove()
    tmpfile2.remove()
