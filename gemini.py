#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=======================
Usage
=======================

Usage:
  gemini.py --title=<title> [--threads=<threads>] [--config=<yaml>] <files>...

Options:
  <files>...
  --title = <title>      The title of report
  --threads = <threads>  The number of threads in challenge [default: 1]
  --config = <yaml>      Configuration file(see below) [default: config.yaml]


=======================
Config file definition
=======================

one:
  name: total
  host: http://api.navitime.jp/v1/00001014
  # proxy: null
other:
  name: transfer
  host: http://api.navitime.jp/v1/00002005
  # proxy: null
input:
  encoding: utf8
  # plan / csv / json / yaml
  format: csv
output:
  encoding: utf8
  response_dir: response
# logger:
#   (See http://wingware.com/psupport/python-manual/3.4/library/logging.config.html#logging-config-dictschema)
addons:
# after:
#   - name: addons.gemini-viewer-addon
#     config:
#       aws_access_key_id: aaaaaaaaaaaa
#       aws_secret_access_key: ssssssssssssssssssssssssssss
#       region: ap-northeast-1
#       table:  dynamo-db-table-name
#       bucket: s3-bucket-name



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
import hashlib
from importlib import import_module
from logging import getLogger
import logging.config

import urllib.parse as urlparser
import requests
from owlmixin.owlcollections import TList
from owlmixin.util import O
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from multiprocessing import Pool
from concurrent import futures
from datetime import datetime
from fn import _

import xmltodict
from xml.dom import minidom
from xml.etree import ElementTree
from docopt import docopt

from modules.dictutils import DictUtils
from modules import requestcreator
from modules.models import *


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


def challenge(args):
    """TODO: Assign types
    Arguments:
       (dict) args
         - (int) seq
         - (str) key
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

    url_one = f'{args["host_one"]}{args["path"]}?{qs_str}'
    url_other = f'{args["host_other"]}{args["path"]}?{qs_str}'

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
        status = "same_without_order"
    else:
        status = "different"

    # Write response body to file
    file_one, file_other = None, None
    dir = os.path.join(args["res_dir"], args["key"])
    if status != Status.SAME:
        file_one = f"one{args['seq']}"
        file_other = f"other{args['seq']}"
        write_to_file(file_one, dir, pretty(res_one), args['output_encoding'])
        write_to_file(file_other, dir, pretty(res_other), args['output_encoding'])

    return create_trial(res_one, res_other, file_one, file_other,
                        status, req_time, args['path'], args['qs'], args['headers'])


def exec(args: Args, key: str) -> Report:
    # Provision
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))

    # Parse inputs to args of multi-thread executor.
    logs = args.files.flat_map(
        lambda f: requestcreator.from_format(f, args.config.input.format, args.config.input.encoding)
    )

    os.mkdir(os.path.join(args.config.output.response_dir, key))
    ex_args = TList(enumerate(logs)).map(lambda x: {
        "seq": x[0] + 1,
        "key": key,
        "session": s,
        "host_one": args.config.one.host,
        "host_other": args.config.other.host,
        "path": x[1].path,
        "qs": x[1].qs,
        "headers": x[1].headers,
        "proxies_one": O(Proxy.from_host(args.config.one.proxy)).then_or_none(lambda x: x.to_dict()),
        "proxies_other": O(Proxy.from_host(args.config.other.proxy)).then_or_none(lambda x: x.to_dict()),
        "output_encoding": args.config.output.encoding,
        "res_dir": args.config.output.response_dir
    })

    # Challenge
    start_time = now()
    with futures.ThreadPoolExecutor(max_workers=args.threads) as ex:
        trials = TList([r for r in ex.map(challenge, ex_args)])
    end_time = now()

    summary = Summary.from_dict({
        "one": {
            "name": args.config.one.name,
            "host": args.config.one.host,
            "proxy": args.config.one.proxy
        },
        "other": {
            "name": args.config.other.name,
            "host": args.config.other.host,
            "proxy": args.config.other.proxy
        },
        "status": trials.group_by(_['status']).map_values(len).to_dict(),
        "time": {
            "start": start_time.strftime("%Y/%m/%d %X"),
            "end": end_time.strftime("%Y/%m/%d %X"),
            "elapsed_sec": (end_time - start_time).seconds
        }
    })

    return Report.from_dict({
        "key": key,
        "title": args.title,
        "summary": summary.to_dict(),
        "trials": trials
    })


if __name__ == '__main__':
    args: Args = Args.from_dict(docopt(__doc__, version=VERSION))
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=args.config.output.encoding)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=args.config.output.encoding)

    # Logging settings load
    logger_config = args.config.output.logger
    if logger_config:
        logging.config.dictConfig(logger_config)

    def apply_after_addon(r: Report, a: Addon):
        return getattr(import_module(a.name), a.command)(r, a.config, args.config.output)

    key = hashlib.sha256((str(now()) + args.to_json()).encode()).hexdigest()
    report: Report = O(args.config.addons) \
        .then(_.after) \
        .or_(TList()) \
        .reduce(apply_after_addon, exec(args, key))

    print(report.to_pretty_json())
