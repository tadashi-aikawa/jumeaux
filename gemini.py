#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=======================
Usage
=======================

Usage:
  gemini.py [--title=<title>] [--threads=<threads>] [--config=<yaml>] [--interval-sec=<interval_sec>] [<files>...]

Options:
  <files>...
  --title = <title>                The title of report
  --threads = <threads>            The number of threads in challenge [default: 1]
  --interval-sec = <interval_sec>  Interval in seconds between trials [default: 0]
  --config = <yaml>                Configuration file(see below) [default: config.yaml]


=======================
Config file definition
=======================

# base: base_config.yaml
title: test  # Ignore if you specified `--title`
one:
  name: total
  host: http://api.navitime.jp/v1/00001014
  # proxy: null
other:
  name: transfer
  host: http://api.navitime.jp/v1/00002005
  # proxy: null
input_files:  # Ignore if you specified `<files>...`
  - resource/requests.csv
output:
  encoding: utf8
  response_dir: response
# logger:  # (See http://wingware.com/psupport/python-manual/3.4/library/logging.config.html#logging-config-dictschema)
#   version: 1
#   formatters:
#     simple:
#       format: '%(levelname)s %(message)s'
#   handlers:
#     console:
#       class : logging.StreamHandler
#       formatter: simple
#       level   : INFO
#       stream  : ext://sys.stderr
#   root:
#     level: INFO
#     handlers: [console]
addons:
  log:
    name: addons.log.csv_addon
    config:
      encoding: utf8
# after:
#   - name: addons.after.gemini_viewer_addon
#     config:
#       table:  dynamo-db-table-name
#       bucket: s3-bucket-name
"""

import sys
import io
import json
import os
import hashlib
from importlib import import_module
from logging import getLogger
import logging.config


import requests
import urllib.parse as urlparser
import time
from owlmixin.owlcollections import TList
from owlmixin.util import O, load_yamlf
from deepdiff import DeepDiff
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from multiprocessing import Pool
from concurrent import futures
from datetime import datetime
from fn import _

import xmltodict
from docopt import docopt

from modules.dictutils import DictUtils
from modules.models import *


VERSION = "0.9.5"
MAX_RETRIES = 3
logger = getLogger(__name__)


def now():
    """
    For test
    """
    return datetime.today()


def addon_log(func):
    def wrapper(*args, **kwargs):
        addon_name = TList(args).find(lambda x: isinstance(x, Addon)).name
        logger.debug(f'********** Start {addon_name} **********')
        result = func(*args, **kwargs)
        logger.debug(f'********** End   {addon_name} **********')
        return result
    return wrapper


@addon_log
def apply_log_addon(file: str, a: Addon):
    return getattr(import_module(a.name), a.command)(file, a.config)


@addon_log
def apply_request_addon(requests: TList[Request], a: Addon):
    return getattr(import_module(a.name), a.command)(requests, a.config)


@addon_log
def apply_res2dict_addon(payload: Res2DictAddOnPayload, a: Addon):
    return getattr(import_module(a.name), a.command)(payload, a.config)


@addon_log
def apply_judgement_addon(payload: JudgementAddOnPayload, a: Addon):
    return getattr(import_module(a.name), a.command)(payload, a.config)


@addon_log
def apply_dump_addon(payload: ResponseAddOnPayload, a: Addon):
    return getattr(import_module(a.name), a.command)(payload, a.config)


@addon_log
def apply_after_addon(r: Report, a: Addon, summary: OutputSummary):
    return getattr(import_module(a.name), a.command)(r, a.config, summary)


def write_to_file(name, dir, body):
    with open(f'{dir}/{name}', "bw") as f:
        f.write(body)


def make_dir(path):
    os.makedirs(path)
    os.chmod(path, 0o777)


def http_get(args):
    session, url, headers, proxies = args
    try:
        r = session.get(url, headers=headers, proxies=proxies)
    finally:
        session.close()
    return r


def to_sec(elapsed):
    return round(elapsed.seconds + elapsed.microseconds / 1000000, 2)


def concurrent_request(session, headers, url_one, url_other, proxies_one, proxies_other):
    pool = Pool(2)
    fs = ((session, url_one, headers, proxies_one),
          (session, url_other, headers, proxies_other))
    try:
        logger.info(f"Request one:   {url_one}")
        logger.info(f"Request other: {url_other}")
        res_one, res_other = pool.imap(http_get, fs)
        logger.info(f"Response one:   {res_one.status_code} / {to_sec(res_one.elapsed)}s / {len(res_one.content)}b / {res_one.headers.get('content-type')}")
        logger.info(f"Response other: {res_other.status_code} / {to_sec(res_other.elapsed)}s / {len(res_other.content)}b / {res_other.headers.get('content-type')}")
    finally:
        pool.close()

    return res_one, res_other


def challenge(arg: ChallengeArg) -> Trial:
    logger.debug(f"Sleep:  {arg.interval_sec} sec")
    time.sleep(arg.interval_sec)
    logger.info(f"Challenge:  {arg.seq} / {arg.number_of_request} -- {arg.name}")

    qs_str = urlparser.urlencode(arg.qs, doseq=True)

    url_one = f'{arg.host_one}{arg.path}?{qs_str}'
    url_other = f'{arg.host_other}{arg.path}?{qs_str}'

    # Get two responses
    req_time = now()
    try:
        res_one, res_other = concurrent_request(arg.session, arg.headers,
                                                url_one, url_other,
                                                arg.proxy_one, arg.proxy_other)
    except ConnectionError:
        # TODO: Integrate logic into create_trial
        return Trial.from_dict({
            "seq": arg.seq,
            "name": arg.name,
            "request_time": req_time.strftime("%Y/%m/%d %X"),
            "status": Status.FAILURE,
            "path": arg.path,
            "queries": arg.qs,
            "headers": arg.headers,
            "one": {
                "url": url_one
            },
            "other": {
                "url": url_other
            }
        })

    def res2dict(res) -> Optional[dict]:
        payload = Res2DictAddOnPayload.from_dict({
            "response": res,
            "result": None
        })
        return O(arg.addons).then(_.res2dict).or_(TList()) \
            .reduce(apply_res2dict_addon, payload) \
            .result

    dict_one = res2dict(res_one)
    dict_other = res2dict(res_other)

    # Create diff
    ddiff = DeepDiff(dict_one, dict_other) \
        if dict_one is not None and dict_other is not None \
        else None
    diff_keys: Optional[DiffKeys] = DiffKeys.from_dict({
        "changed": TList(ddiff.get('type_changes', {}).keys() | ddiff.get('values_changed', {}).keys())
            .map(lambda x: x.replace('[', '<').replace(']', '>'))
            .order_by(_),
        "added": TList(ddiff.get('dictionary_item_added', {}) | ddiff.get('iterable_item_added', {}).keys())
            .map(lambda x: x.replace('[', '<').replace(']', '>'))
            .order_by(_),
        "removed": TList(ddiff.get('dictionary_item_removed', {}) | ddiff.get('iterable_item_removed', {}).keys())
            .map(lambda x: x.replace('[', '<').replace(']', '>'))
            .order_by(_)
    }) if ddiff is not None else None

    def judge(r_one, r_other) -> Status:
        payload = JudgementAddOnPayload.from_dict({
            "path": arg.path,
            "qs": arg.qs,
            "headers": arg.headers,
            "res_one": r_one,
            "res_other": r_other,
            "diff_keys": O(diff_keys).then_or_none(lambda x: x.to_dict()),
            "regard_as_same": r_one.content == r_other.content
        })
        regard_as_same: bool = O(arg.addons).then(_.judgement).or_(TList()) \
            .reduce(apply_judgement_addon, payload) \
            .regard_as_same
        return Status.SAME if regard_as_same else Status.DIFFERENT

    # Judgement
    status: Status = judge(res_one, res_other)
    logger.info(f"Status:   {status.value}")

    # Write response body to file
    def pretty(res):
        payload = ResponseAddOnPayload.from_dict({
            "response": res,
            "body": res.content,
            "encoding": res.encoding
        })
        return O(arg.addons).then(_.dump).or_(TList()) \
            .reduce(apply_dump_addon, payload) \
            .body

    file_one = file_other = None
    if status != Status.SAME:
        dir = f'{arg.res_dir}/{arg.key}'
        file_one = f'one/({arg.seq}){arg.name}'
        file_other = f'other/({arg.seq}){arg.name}'
        write_to_file(file_one, dir, pretty(res_one))
        write_to_file(file_other, dir, pretty(res_other))

    return Trial.from_dict({
        "seq": arg.seq,
        "name": arg.name,
        "request_time": req_time.strftime("%Y/%m/%d %X"),
        "status": status,
        "path": arg.path or "No path",
        "queries": arg.qs,
        "headers": arg.headers,
        "diff_keys": O(diff_keys).then_or_none(lambda x: x.to_dict()),
        "one": {
            "url": res_one.url,
            "status_code": res_one.status_code,
            "byte": len(res_one.content),
            "response_sec": to_sec(res_one.elapsed),
            "content_type": res_one.headers.get("content-type"),
            "file": file_one
        },
        "other": {
            "url": res_other.url,
            "status_code": res_other.status_code,
            "byte": len(res_other.content),
            "response_sec": to_sec(res_other.elapsed),
            "content_type": res_other.headers.get("content-type"),
            "file": file_other
        }
    })


def exec(args: Args, config: Config, log_file_paths: TList[str], key: str) -> Report:
    # Provision
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))

    origin_logs = log_file_paths.flat_map(
        lambda f: apply_log_addon(f, config.addons.log)
    )

    logs = O(config.addons).then(_.request).or_(TList()) \
        .reduce(apply_request_addon, origin_logs)

    make_dir(f'{config.output.response_dir}/{key}/one')
    make_dir(f'{config.output.response_dir}/{key}/other')

    # Parse inputs to args of multi-thread executor.
    ex_args = TList(enumerate(logs)).map(lambda x: {
        "seq": x[0] + 1,
        "number_of_request": len(logs),
        "key": key,
        "name": x[1].name or str(x[0] + 1),
        "session": s,
        "host_one": config.one.host,
        "host_other": config.other.host,
        "path": x[1].path,
        "qs": x[1].qs,
        "headers": x[1].headers,
        "proxy_one": Proxy.from_host(config.one.proxy),
        "proxy_other": Proxy.from_host(config.other.proxy),
        "res_dir": config.output.response_dir,
        "addons": config.addons,
        "interval_sec": args.interval_sec
    })

    # Challenge
    start_time = now()
    with futures.ThreadPoolExecutor(max_workers=args.threads) as ex:
        trials = TList([r for r in ex.map(challenge, ChallengeArg.from_dicts(ex_args))])
    end_time = now()

    summary = Summary.from_dict({
        "one": {
            "name": config.one.name,
            "host": config.one.host,
            "proxy": config.one.proxy
        },
        "other": {
            "name": config.other.name,
            "host": config.other.host,
            "proxy": config.other.proxy
        },
        "status": trials.group_by(_.status.value).map_values(len).to_dict(),
        "paths": trials.group_by(_.path).map_values(len).to_dict(),
        "time": {
            "start": start_time.strftime("%Y/%m/%d %X"),
            "end": end_time.strftime("%Y/%m/%d %X"),
            "elapsed_sec": (end_time - start_time).seconds
        }
    })

    return Report.from_dict({
        "key": key,
        "title": args.title or config.title or "No title",
        "summary": summary.to_dict(),
        "trials": trials.to_dicts(),
        "addons": config.addons.to_dict()
    })


def hash_from_args(args: Args) -> str:
    return hashlib.sha256((str(now()) + args.to_json()).encode()).hexdigest()


def create_config(config_path: str):
    origin_config = load_yamlf(config_path, 'utf8')
    base_config_path = origin_config.get('base')

    if not base_config_path:
        return Config.from_dict(origin_config)

    base_config = load_yamlf(f'{os.path.dirname(config_path)}/{base_config_path}', 'utf8')
    base_config.update(origin_config)
    return Config.from_dict(base_config)


if __name__ == '__main__':
    args: Args = Args.from_dict(docopt(__doc__, version=VERSION))
    config: Config = create_config(args.config)

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=config.output.encoding)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=config.output.encoding)

    # Logging settings load
    logger_config = config.output.logger
    if logger_config:
        logger_config.update({'disable_existing_loggers': False})
        logging.config.dictConfig(logger_config)

    input_paths = args.files or config.input_files.map(
        lambda f: f'{os.path.dirname(args.config)}/{f}'
    )

    report: Report = O(config.addons).then(_.after).or_(TList()) \
        .reduce(lambda t, x: apply_after_addon(t, x, config.output), exec(args, config, input_paths, hash_from_args(args)))

    print(report.to_pretty_json())
