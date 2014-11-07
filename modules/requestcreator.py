# -*- coding:utf-8 -*-


"""
Usage:
Each function returns the format of the following.

[
    {
        "path": "/path",
        "qs": 'a=1&b=2'
    },
    ・
    ・
    {
        "path": "/path",
        "qs": ''
    }
]

"qs" never be None.
"""

import yaml


def from_apache_accesslog(f):
    """Transform apache access_log.

    Arguments:
        (file) f: Access log file

    Returns:
        (dict): Refer to `Usage`.

    Exception:
        ValueError: If url is invalid.
    """
    return [_from_apache_accesslog(r) for r in f]


def from_yaml(f):
    """Transform yaml as below.
        - path: "/path1"
          qs: "a=1&b=2"
        - path: "/path2"
          qs: "c=1"
        - path: "/path3"

    Arguments:
        (file) f: yaml

    Returns:
        (dict): Refer to `Usage`.

    Exception:
        ValueError: If path does not exist.
    """
    rs = yaml.load(f.read())
    for r in rs:
        if 'path' not in r:
            raise ValueError
        if 'qs' not in r:
            r['qs'] = ''

    return rs


def _from_apache_accesslog(r):
    """Transform apache access_log.

    Arguments:
        (str) r: Access log record

    Returns:
        (dict): Refer to `Usage`.

    Exception:
        ValueError: If url is invalid.
    """
    url = r.split(' ')[6]
    if len(url.split('?')) > 2:
        raise ValueError

    path = url.split('?')[0]
    qs = url.split('?')[1] if len(url.split('?')) == 2 else ''

    return {
        "path": path,
        "qs": qs
    }
