#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=======================
Usage
=======================

Usage:
  gemini.py [--threads=<threads>] [--config=<json>] <files>...

Options:
  <files>...
  --threads = <threads>  The number of threads in challenge [default: 1]
  --config = <json>      Configuration file(see below) [default: config.json]


=======================
Config file definition
=======================

Set following value as default if property is blank and not REQUIRED.

{
    "one": {
        "host": "http://one",  # (REQUIRED)
        "proxy": null
    },
    "other": {
        "host": "http://other",  # (REQUIRED)
        "proxy": null
    },
    "input": {
        "format": "plain",  # (see `Input format`)
        "encoding": "utf8"
    },
    "output": {
        "encoding": "utf8",
        "response": {
            "dir": "response"    # (REQUIRED)
        },
        "logger": {
            # (See http://wingware.com/psupport/python-manual/3.4/library/logging.config.html#logging-config-dictschema)
        }
    }
}

=======================
Input format
=======================

Correspond to following format.

1. plain
---------

"/path1?a=1&b=2"
"/path2?c=1"
"/path3"

2. apache
---------

000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path2?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"

3. yaml
---------

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

4. csv
---------

"/path1","a=1&b=2","header1=1&header2=2"
"/path2","c=1"
"/path3",,"header1=1&header2=2"
"/path4"

"""

import codecs
import sys
import io
import json
import os
from logging import getLogger
import logging.config

import urllib.parse as urlparser
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from multiprocessing import Pool
from concurrent import futures
from datetime import datetime

import xmltodict
from xml.dom import minidom
from xml.etree import ElementTree

from docopt import docopt
from schema import Schema, Or, And, Use, SchemaError

from modules.dictutils import DictUtils
from modules import requestcreator


VERSION = "0.9.5"
MAX_RETRIES = 3
logger = getLogger(__name__)


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


def pretty(res):
    mime_type = res.headers['content-type'].split(';')[0]
    if mime_type in ('text/json', 'application/json'):
        return json.dumps(res.json(), ensure_ascii=False, indent=4, sort_keys=True)
    elif mime_type in ('text/xml', 'application/xml'):
        tree = ElementTree.XML(res.text)
        return minidom.parseString(ElementTree.tostring(tree)).toprettyxml(indent='    ')
    else:
        # TODO: If binary, return res.content or None
        return res.text


def write_to_file(name, dir, body, encoding):
    with codecs.open(os.path.join(dir, name), "w", encoding=encoding) as f:
        f.write(body)


def create_trial(res_one, res_other, file_one, file_other,
                 status, req_time, path, qs, headers):
    trial = {
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
    if file_one is not None:
        trial['one']['file'] = file_one
    if file_other is not None:
        trial['other']['file'] = file_other
    return trial


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
    doc = docopt(__doc__, version=VERSION)

    pre_schema = Schema({
        '<files>': [str],
        '--config': Use(open),
        '--threads': And(Use(int), lambda n: n > 0)
    })
    try:
        pre_args = pre_schema.validate(doc)
        config = json.load(pre_args['--config'])
    except SchemaError as e:
        print(e)
        sys.exit(1)

    args = {
        'files': pre_args['<files>'],
        'host_one': config['one']['host'],
        'host_other': config['other']['host'],
        'proxy_one': config['one'].get('proxy', None),
        'proxy_other': config['other'].get('proxy', None),
        'input_encoding': config['input'].get('encoding', 'utf-8'),
        'output_encoding': config['output'].get('encoding', 'utf-8'),
        "logger": config['output'].get('logger', None),
        'res_dir': config['output']['response'].get('dir', 'response'),
        'input_format': config['input'].get('format', 'plain'),
        'threads': pre_args['--threads']
    }

    schema = Schema({
        'files': [Use(open)],
        'host_one': str,
        'host_other': str,
        'proxy_one': Or(None, str),
        'proxy_other': Or(None, str),
        'input_encoding': str,
        'output_encoding': str,
        'logger': Or(None, dict),
        'res_dir': os.path.exists,
        'input_format': Or('plain', 'apache', 'yaml', 'csv'),
        'threads': And(Use(int), lambda n: n > 0)
    })

    try:
        return schema.validate(args)
    except SchemaError as e:
        print(e)
        sys.exit(1)


def challenge(args):
    """
    Arguments:
       (dict) args
         - (int) seq
         - (session) session
         - (str) host_one
         - (str) host_other
         - (str) path
         - (str) output_encoding
         - (str) res_dir
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
    req_time = now()
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
    if diff is not None and len(diff) == 0:
        status = "same"
    elif diff_without_order is not None and len(diff_without_order) == 0:
        status = "same without order"
    else:
        status = "different"

    # Write response body to file
    file_one, file_other = None, None
    if status != "same":
        file_one = "one{}".format(args['seq'])
        file_other = "other{}".format(args['seq'])
        write_to_file(file_one, args['res_dir'], pretty(res_one), args['output_encoding'])
        write_to_file(file_other, args['res_dir'], pretty(res_other), args['output_encoding'])

    return create_trial(res_one, res_other, file_one, file_other,
                        status, req_time, args['path'], args['qs'], args['headers'])


def main(args):
    # Provision
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    proxies_one = create_proxies(args['proxy_one'])
    proxies_other = create_proxies(args['proxy_other'])

    # Parse inputs to args of multi-thread executor.
    logs = []
    for f in args['files']:
        logs.extend(requestcreator.from_format(f, args['input_format']))

    ex_args = [{
               "seq": i + 1,
               "session": s,
               "host_one": args['host_one'],
               "host_other": args['host_other'],
               "path": l['path'],
               "qs": l['qs'],
               "headers": l['headers'],
               "proxies_one": proxies_one,
               "proxies_other": proxies_other,
               "output_encoding": args['output_encoding'],
               "res_dir": args['res_dir']
               } for i, l in enumerate(logs)]

    # Challenge
    start_time = now()
    with futures.ThreadPoolExecutor(max_workers=args['threads']) as ex:
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
                "host": args['host_one'],
                "proxy": args['proxy_one']
            },
            "other": {
                "host": args['host_other'],
                "proxy": args['proxy_other']
            }
        },
        "trials": trials
    }

    # Output result
    print(json.dumps(result, indent=4, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    args = create_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=args['output_encoding'])
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=args['output_encoding'])

    # Logging settings load
    logger_config = args.get('logger')
    if (logger_config is not None):
        logging.config.dictConfig(logger_config)

    main(args)
