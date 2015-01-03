#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gemini

Usage:
gemini --host-one=<host_one> --host-other=<host_other> --report <report> <files>...
                      [--input-format=<input_format>]
                      [--proxy-one=<proxy_one>] [--proxy-other=<proxy_other>]
                      [--input-encoding=<input_encoding>] [--output-encoding=<output_encoding>]
                      [--threads=<threads>]

Options:
<files>...
--host-one = <host_one>                   One host
--host-other = <host_other>               Other host
--proxy-one = <proxy_one>                 Proxy for one host
--proxy-other = <proxy_other>             Proxy for other host
--input-format = <input_format>           Input file format [default: apache]
--input-encoding = <input_encoding>       Input file encoding [default: utf8]
--output-encoding = <output_encoding>     Output json encoding [default: utf8]
--threads = <threads>                     The number of threads in challenge [default: 1]
--report = <report>                       Output json file
"""

import codecs
import sys
import io
import json

import urllib.parse as urlparser
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from multiprocessing import Pool
from concurrent import futures
from datetime import datetime

import xmltodict

from docopt import docopt
from schema import Schema, Or, And, Use, SchemaError

from modules.dictutils import DictUtils
from modules import requestcreator


VERSION = "0.9.0"
MAX_RETRIES = 3


def now():
    """
    For test
    """
    return datetime.today()


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


def create_trial(res_one, res_other, status, req_time, path, qs, headers):
    return {
        "request_time": req_time.strftime("%Y/%m/%d %X"),
        "status": status,
        "path": path,
        "queries": qs,
        "headers": headers,
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


def concurrent_request(session, headers, url_one, url_other, proxies_one, proxies_other):
    pool = Pool(2)
    fs = ((session, url_one, headers, proxies_one),
          (session, url_other, headers, proxies_other))
    try:
        res_one, res_other = pool.imap(http_get, fs)
    finally:
        pool.close()

    return res_one, res_other


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
        '--threads': And(Use(int), lambda n: n > 0),
        '--report': str
    })
    try:
        args = schema.validate(docopt(__doc__, version=VERSION))
    except SchemaError as e:
        print(e)
        sys.exit(1)

    return args


def challenge(args):
    """
    Arguments:
       (dict) args
         - (session) session
         - (str) host_one
         - (str) host_other
         - (str) path
         - (dict) qs
           - (str) key of query
           - ...
         - (dict) headers
           - (str) key of header
           - ...
         - (dict) proxies_one
           - (str) http
           - (str) https
         - (dict) proxies_other
           - (str) http
           - (str) https
    """
    qs_str = urlparser.urlencode(args['qs'], doseq=True)

    url_one = '{0}{1}?{2}'.format(args['host_one'], args['path'], qs_str)
    url_other = '{0}{1}?{2}'.format(args['host_other'], args['path'], qs_str)

    # Get two responses
    req_time = datetime.today()
    try:
        res_one, res_other = concurrent_request(args['session'], args['headers'],
                                                url_one, url_other,
                                                args['proxies_one'], args['proxies_other'])
    except ConnectionError:
        # TODO: Integrate logic into create_trial
        return {
            "request_time": req_time.strftime("%Y/%m/%d %X"),
            "status": "failure",
            "path": args['path'],
            "queries": args['qs'],
            "headers": args['headers'],
            "one": {
                "url": url_one
            },
            "other": {
                "url": url_other
            }
        }

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

    return create_trial(res_one, res_other, status, req_time, args['path'], args['qs'], args['headers'])


def main():
    args = create_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=args['--output-encoding'])

    # Provision
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    proxies_one = create_proxies(args['--proxy-one'])
    proxies_other = create_proxies(args['--proxy-other'])

    # Parse inputs to args of multi-thread executor.
    logs = []
    for f in args['<files>']:
        logs.extend(requestcreator.from_format(f, args['--input-format']))

    ex_args = [{
               "session": s,
               "host_one": args['--host-one'],
               "host_other": args['--host-other'],
               "path": l['path'],
               "qs": l['qs'],
               "headers": l['headers'],
               "proxies_one": proxies_one,
               "proxies_other": proxies_other
               } for l in logs]

    # Challenge
    start_time = now()
    with futures.ThreadPoolExecutor(max_workers=args['--threads']) as ex:
        trials = [r for r in ex.map(challenge, ex_args)]
    end_time = now()

    result = {
        "summary": {
            "time": {
                "start": start_time.strftime("%Y/%m/%d %X"),
                "end": end_time.strftime("%Y/%m/%d %X"),
                "elapsed_sec": (end_time - start_time).seconds
            },
            "one": {
                "host": args['--host-one'],
                "proxy": args['--proxy-one']
            },
            "other": {
                "host": args['--host-other'],
                "proxy": args['--proxy-other']
            }
        },
        "trials": trials
    }

    # Output result
    with codecs.open(args['--report'], 'w', encoding=args['--output-encoding']) as f:
        json.dump(result, f, indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == '__main__':
    main()
