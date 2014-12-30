# -*- coding:utf-8 -*-


"""
Usage:
Each function returns the format of the following.

[
    {
        "path": "/path",
        "qs": {
            "q1": ["v1"],
            "q2": ["v2", "v3"]
        }
        "headers": {
            "key1": "value1",
            "key2": "value2"
        }
    },
    ・
    ・
    {
        "path": "/path",
        "qs": {},
        "headers": {}
    }
]

"qs" never be None.
"""

import yaml
import csv


def from_format(file, format):
    """Transform any formatted file into request list.
       Support for
       * apache
       * yaml
       * csv

    Arguments:
        (file) file: file
        (Str)  format: format

    Returns:
        list(dict): Refer to `Usage`.

    Exception:
        ValueError: If format is invalid.
    """
    functions = {
        'apache': _from_apache_accesslog,
        'yaml': _from_yaml,
        'csv': _from_csv,
    }
    if format not in functions:
        raise ValueError

    return functions[format](file)


def _from_apache_accesslog(f):
    """Transform apache access_log as below.
        000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"
        000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /test2?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)"

    Arguments:
        (file) f: Access log file

    Returns:
        list(dict): Refer to `Usage`.

    Exception:
        ValueError: If url is invalid.
    """
    outputs = []
    for r in f:
        url = r.split(' ')[6]
        if len(url.split('?')) > 2:
            raise ValueError

        path = url.split('?')[0]
        qs = url.split('?')[1] if len(url.split('?')) == 2 else ''

        outputs.append({"path": path, "qs": qs})
    return outputs


def _from_yaml(f):
    """Transform yaml as below.
        - path: "/path1"
          qs:
            q1:
              - v1
            q2:
              - v2
              - v3
          headers:
            key1: "header1"
            key2: "header2"
        - path: "/path2"
          qs:
            q1:
              - v1
        - path: "/path3"
          headers:
            key1: "header1"
            key2: "header2"
        - path: "/path4"

    Arguments:
        (file) f: yaml

    Returns:
        list(dict): Refer to `Usage`.

    Exception:
        ValueError: If path does not exist.
    """
    rs = yaml.load(f.read())
    for r in rs:
        if 'path' not in r:
            raise ValueError
        if 'qs' not in r:
            r['qs'] = {}
        if 'headers' not in r:
            r['headers'] = {}

    return rs


def _from_csv(f):
    """Transform csv as below.
        "/path1","a=1&b=2"
        "/path2","c=1"
        "/path3",
        "/path4"

    Arguments:
        (file) f: csv

    Returns:
        list(dict): Refer to `Usage`.

    Exception:
        ValueError: If fomat is invalid.
    """
    rs = csv.DictReader(f, ('path', 'qs'), restval='')

    outputs = []
    for r in rs:
        if len(r) > 2:
            raise ValueError
        outputs.append(r)

    return outputs
