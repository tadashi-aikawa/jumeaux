#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gemini

Usage:
gemini --host-one=<host_one> --host-other=<host_other> --report <report> <files>...
                      [--input-format=<input_format>]
                      [--proxy-one=<proxy_one>] [--proxy-other=<proxy_other>]
                      [--input-encoding=<input_encoding>] [--output-encoding=<output_encoding>]

Options:
<files>...
--host-one = <host_one>                   One host
--host-other = <host_other>               Other host
--proxy-one = <proxy_one>                 Proxy for one host
--proxy-other = <proxy_other>             Proxy for other host
--input-format = <input_format>           Input file format [default: apache]
--input-encoding = <input_encoding>       Input file encoding [default: utf8]
--output-encoding = <output_encoding>     Output json encoding [default: utf8]
--report = <report>                       Output json file
"""

import codecs
import sys
import io
import datetime
import json

import urllib.parse as urlparser
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from multiprocessing import Pool

import xmltodict

from docopt import docopt
from schema import Schema, Or, Use, SchemaError

from modules.dictutils import DictUtils
from modules import requestcreator


VERSION = "0.5.0"
MAX_RETRIES = 3


def create_diff(text1, text2, ignore_properties, ignore_order=False):
    """
    Arguments:
       (str) text1                    -- Target one
       (str) text2                    -- Target other
       (list(str)) ignore_properties  -- Ignore properties
       (bool) ignore_order            -- Ignore order in array

    Returns:
       (list(str)) --- Diff string (Empty list if same. None if cannot be analyzed and different.)
    """
    if text1 == text2:
        return []

    try:
        return DictUtils.diff(json.loads(text1), json.loads(text2),
                              ignore_properties=ignore_properties,
                              ignore_order=ignore_order)
    except:
        pass

    try:
        return DictUtils.diff(xmltodict.parse(text1), xmltodict.parse(text2),
                              ignore_properties=ignore_properties,
                              ignore_order=ignore_order)
    except:
        pass

    return None


def create_trial(res_one, res_other, status, req_time, path, qs):
    return {
        "request_time": req_time.strftime("%Y/%m/%d %X"),
        "status": status,
        "path": path,
        "queries": urlparser.parse_qs(qs),
        "one": {
            "url": res_one.url,
            "status_code": res_one.status_code,
            "byte": len(res_one.content),
            "response_sec": round(res_one.elapsed.seconds + res_one.elapsed.microseconds / 1000000, 2)
        },
        "other": {
            "url": res_other.url,
            "status_code": res_other.status_code,
            "byte": len(res_other.content),
            "response_sec": round(res_other.elapsed.seconds + res_other.elapsed.microseconds / 1000000, 2)
        }
    }


def http_get(args):
    session, url, headers, proxies = args
    try:
        r = session.get(url, headers=headers, proxies=proxies)
    finally:
        session.close()
    return r


def create_proxies(proxy):
    p = dict()
    if proxy:
        p['http'] = "http://{0}".format(proxy)
        p['https'] = "https://{0}".format(proxy)

    return p


def create_args():
    schema = Schema({
        '<files>': [Use(open)],
        '--host-one': str,
        '--host-other': str,
        '--proxy-one': Or(None, str),
        '--proxy-other': Or(None, str),
        '--input-format': Or('apache', 'yaml', 'csv'),
        '--input-encoding': str,
        '--output-encoding': str,
        '--report': str
    })
    try:
        args = schema.validate(docopt(__doc__, version=VERSION))
    except SchemaError as e:
        print(e)
        sys.exit(1)

    return args


def challenge(session, host_one, host_other, path, qs, proxies_one={}, proxies_other={}):
    url_one = '{0}{1}?{2}'.format(host_one, path, qs)
    url_other = '{0}{1}?{2}'.format(host_other, path, qs)

    headers = []  # TODO: headers

    # Get two responses
    req_time = datetime.datetime.today()
    pool = Pool(2)
    fs = ((session, url_one, headers, proxies_one),
          (session, url_other, headers, proxies_other))
    try:
        res_one, res_other = pool.imap(http_get, fs)
    except ConnectionError:
        # TODO: Integrate logic into create_trial
        return {
            "request_time": req_time.strftime("%Y/%m/%d %X"),
            "status": "failure",
            "path": path,
            "queries": urlparser.parse_qs(qs),
            "one": {
                "url": url_one
            },
            "other": {
                "url": url_other
            }
        }
    finally:
        pool.close()

    # Create diff
    ignore_properties = []  # Todo ignore_properties
    diff = create_diff(res_one.text, res_other.text, ignore_properties)
    diff_without_order = create_diff(res_one.text, res_other.text,
                                     ignore_properties, True)

    # Judgement
    status = "different"
    if diff_without_order is not None and len(diff_without_order) == 0:
        status = "same without order"
    if diff is not None and len(diff) == 0:
        status = "same"

    return create_trial(res_one, res_other, status, req_time, path, qs)


def main():
    args = create_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=args['--output-encoding'])

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    proxies_one = create_proxies(args['--proxy-one'])
    proxies_other = create_proxies(args['--proxy-other'])

    # parse files to ...
    logs = []
    for f in args['<files>']:
        logs.extend(requestcreator.from_format(f, args['--input-format']))

    trials = [challenge(s, args['--host-one'], args['--host-other'],
                        l['path'], l['qs'],
                        proxies_one, proxies_other)
              for l in logs]

    result = {
        "trials": trials
    }

    json.dump(result, codecs.open(args['--report'], 'w',
              encoding=args['--output-encoding']),
              indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == '__main__':
    main()
