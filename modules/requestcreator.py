# -*- coding:utf-8 -*-

import re
import csv
import urllib.parse as urlparser
from enum import Enum

from modules.models import *


class Format(Enum):
    PLAIN = "plain"
    APACHE = "apache"
    YAML = "yaml"
    CSV = "csv"


def from_format(file: str, format_: Format, encoding: str='utf8') -> TList[Request]:
    """Transform any formatted file into request list.

    :param file: Log file
    :param format_: Log format
    :param encoding: Log encoding
    :return: Requests
    """
    functions = {
        Format.PLAIN: _from_plain,
        Format.APACHE: _from_apache_accesslog,
        Format.YAML: _from_yaml,
        Format.CSV: _from_csv,
    }
    if format_ not in functions:
        raise ValueError

    return functions[format_](file, encoding)


def _from_plain(file: str, encoding: str) -> TList[Request]:
    """Transform plain as below.

    :param file:
    :param encoding:
    :return: Requests
    """
    def line_to_request(line: str) -> Request:
        path = line.split('?')[0]
        qs = urlparser.parse_qs(line.split('?')[1]) if len(line.split('?')) > 1 else {}
        return Request.from_dict({"path": path, "qs": qs, "headers": {}})

    with open(file, encoding=encoding) as f:
        requests: TList[Request] = TList([x.rstrip() for x in f if x != '\n']).map(line_to_request)

    return requests


def _from_apache_accesslog(file: str, encoding: str) -> TList[Request]:
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


def _from_yaml(file: str, encoding: str) -> TList[Request]:
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


def _from_csv(file: str, encoding: str) -> TList[Request]:
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
