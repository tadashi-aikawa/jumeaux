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

"qs" and "headers" never be None.
"""

import re
import csv
import urllib.parse as urlparser

from modules.models import *


def from_format(file: Text, format: Text, encoding: Text='utf8') -> TList[Request]:
    """Transform any formatted file into request list.
       Support for
       * plain
       * apache
       * yaml
       * csv

    Exception:
        ValueError: If format is invalid.
    """
    functions = {
        'plain': _from_plain,
        'apache': _from_apache_accesslog,
        'yaml': _from_yaml,
        'csv': _from_csv,
    }
    if format not in functions:
        raise ValueError

    return functions[format](file, encoding)


def _from_plain(file: Text, encoding: Text) -> TList[Request]:
    """Transform plain as below.
        "/path1?a=1&b=2"
        "/path2?c=1"
        "/path3"
    """
    outputs = []
    with open(file, encoding=encoding) as f:
        for r in [x.rstrip() for x in f if x != '\n']:
            path = r.split('?')[0]
            if len(r.split('?')) > 1:
                qs = urlparser.parse_qs(r.split('?')[1])
            else:
                qs = {}
            outputs.append({"path": path, "qs": qs, "headers": {}})

    return Request.from_dicts(outputs)


def _from_apache_accesslog(file: Text, encoding: Text) -> TList[Request]:
    """Transform apache access_log as below.
        000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
        000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path2?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"

    Exception:
        ValueError: If url is invalid.
    """
    outputs = []
    with open(file, encoding=encoding) as f:
        for r in f:
            url = r.split(' ')[6]
            if len(url.split('?')) > 2:
                raise ValueError

            path = url.split('?')[0]
            if len(url.split('?')) > 1:
                qs = urlparser.parse_qs(url.split('?')[1])
            else:
                qs = {}

            headers = {}
            for h in re.compile('"([^= ]+=[^ ]+)"').findall(r):
                k, v = h.split('=')
                if v != '-':
                    headers[k] = v
            outputs.append({"path": path, "qs": qs, "headers": headers})

    return Request.from_dicts(outputs)


def _from_yaml(file: Text, encoding: Text) -> TList[Request]:
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

    Exception:
        ValueError: If path does not exist.
    """
    try:
        return Request.from_yamlf_to_list(file, encoding=encoding)
    except TypeError as e:
        raise ValueError(e)


def _from_csv(file: Text, encoding: Text) -> TList[Request]:
    """Transform csv as below.
        "/path1","a=1&b=2","header1=1&header2=2"
        "/path2","c=1"
        "/path3",,"header1=1&header2=2"
        "/path4"

    Exception:
        ValueError: If fomat is invalid.
    """
    outputs = []

    with open(file, encoding=encoding) as f:
        rs = csv.DictReader(f, ('path', 'qs', 'headers'), restval={})
        for r in rs:
            if len(r) > 3:
                raise ValueError
            r['qs'] = urlparser.parse_qs(r['qs'])

            # XXX: This is bad implementation but looks simple...
            r['headers'] = urlparser.parse_qs(r['headers'])
            for k, v in r['headers'].items():
                r['headers'][k] = v[0]

            outputs.append(r)

    return Request.from_dicts(outputs)
