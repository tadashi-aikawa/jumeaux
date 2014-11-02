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

If url has no queries, "qs" is empty(not None).
"""

import yaml


class RequestCreator(object):

    @classmethod
    def from_apache_accesslog(cls, f):
        """Transform apache access_log.

        Arguments:
            (file) f: Access log file

        Returns:
            (dict): Refer to `Usage`.

        Exception:
            ValueError: If url is invalid.
        """
        return [cls._from_apache_accesslog(r) for r in f]

    @classmethod
    def from_yaml(cls, f):
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
            ValueError: If url is invalid.
        """
        rs = yaml.load(f.read())
        for r in rs:
            if 'path' not in r:
                raise ValueError
            if 'qs' not in r:
                r['qs'] = ''

        return rs
