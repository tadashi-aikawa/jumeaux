#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=======================
Usage
=======================

Usage:
  jumeaux --config=<yaml>... [--title=<title>] [--description=<description>] [--threads=<threads>] [<files>...]
  jumeaux retry  [--title=<title>] [--description=<description>] [--threads=<threads>] <report>

Options:
  <files>...
  --config = <yaml>...             Configuration files(see below)
  --title = <title>                The title of report
  --description = <description>    The description of report
  --threads = <threads>            The number of threads in challenge
  <report>                         Report for retry
"""


import hashlib
import io
import logging.config
import sys
import urllib.parse as urlparser
import datetime

import os
import requests
from concurrent import futures
from deepdiff import DeepDiff
from docopt import docopt
from fn import _
from logging import getLogger
from owlmixin.util import load_yamlf
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)
from jumeaux import __version__
from jumeaux.addons import AddOnExecutor
from jumeaux.models import *

MAX_RETRIES = 3
logger = getLogger(__name__)
global_addon_executor: AddOnExecutor = None


def now():
    """
    For test
    """
    return datetime.datetime.today()


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
    fs = ((session, url_one, headers, proxies_one),
          (session, url_other, headers, proxies_other))
    with futures.ThreadPoolExecutor(max_workers=2) as ex:
        logger.info(f"Request one:   {url_one}")
        logger.info(f"Request other: {url_other}")
        res_one, res_other = ex.map(http_get, fs)
        logger.info(f"Response one:   {res_one.status_code} / {to_sec(res_one.elapsed)}s / {len(res_one.content)}b / {res_one.headers.get('content-type')}")
        logger.info(f"Response other: {res_other.status_code} / {to_sec(res_other.elapsed)}s / {len(res_other.content)}b / {res_other.headers.get('content-type')}")

    return res_one, res_other


def res2res(res: Response, req: Request):
    return global_addon_executor.apply_res2res(Res2ResAddOnPayload.from_dict({
        "response": res,
        "req": req,
    })).response


def res2dict(res: Response) -> TOption[dict]:
    return global_addon_executor.apply_res2dict(Res2DictAddOnPayload.from_dict({
        "response": res,
        "result": None
    })).result


def judgement(r_one: Response, r_other: Response,
          name: str, path: str, qs: TDict[TList[str]], headers: TList[str],
          diff_keys: Optional[DiffKeys]) -> Status:
    regard_as_same: bool = global_addon_executor.apply_judgement(JudgementAddOnPayload.from_dict({
        "name": name,
        "path": path,
        "qs": qs,
        "headers": headers,
        "res_one": r_one,
        "res_other": r_other,
        "diff_keys": diff_keys,
        "remaining_diff_keys": diff_keys,
        "regard_as_same": r_one.body == r_other.body
    })).regard_as_same
    return Status.SAME if regard_as_same else Status.DIFFERENT


def store_criterion(status: Status, path: str, qs: TDict[TList[str]], headers: TDict[str],
                    r_one: Response, r_other: Response):
    return global_addon_executor.apply_store_criterion(StoreCriterionAddOnPayload.from_dict({
        "status": status,
        "path": path,
        "qs": qs,
        "headers": headers,
        "res_one": r_one,
        "res_other": r_other,
        "stored": False,
    })).stored


def dump(res: Response):
    return global_addon_executor.apply_dump(DumpAddOnPayload.from_dict({
        "response": res,
        "body": res.body,
        "encoding": res.encoding
    })).body


def challenge(arg: ChallengeArg) -> Trial:
    name: str = arg.req.name.get_or(str(arg.seq))

    logger.info(f"Challenge:  {arg.seq} / {arg.number_of_request} -- {name}")

    qs_str = urlparser.urlencode(arg.req.qs, doseq=True)

    url_one = f'{arg.host_one}{arg.req.path}?{qs_str}'
    url_other = f'{arg.host_other}{arg.req.path}?{qs_str}'

    # Get two responses
    req_time = now()
    try:
        r_one, r_other = concurrent_request(arg.session, arg.req.headers,
                                                url_one, url_other,
                                                arg.proxy_one.get(), arg.proxy_other.get())
    except ConnectionError:
        # TODO: Integrate logic into create_trial
        return Trial.from_dict({
            "seq": arg.seq,
            "name": name,
            "request_time": req_time.strftime("%Y/%m/%d %H:%M:%S.%f"),
            "status": Status.FAILURE,
            "path": arg.req.path,
            "queries": arg.req.qs,
            "headers": arg.req.headers,
            "one": {
                "url": url_one
            },
            "other": {
                "url": url_other
            }
        })

    res_one = res2res(Response.from_requests(r_one), arg.req)
    res_other = res2res(Response.from_requests(r_other), arg.req)

    dict_one = res2dict(res_one)
    dict_other = res2dict(res_other)

    # Create diff
    ddiff = DeepDiff(dict_one.get(), dict_other.get()) \
        if not dict_one.is_none() and not dict_other.is_none() \
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

    # Judgement
    status: Status = judgement(res_one, res_other, name, arg.req.path, arg.req.qs, arg.req.headers, diff_keys)
    logger.info(f"Status:   {status.value}")

    file_one = file_other = None
    if store_criterion(status, arg.req.path, arg.req.qs, arg.req.headers, res_one, res_other):
        dir = f'{arg.res_dir}/{arg.key}'
        file_one = f'one/({arg.seq}){name}'
        file_other = f'other/({arg.seq}){name}'
        write_to_file(file_one, dir, dump(res_one))
        write_to_file(file_other, dir, dump(res_other))

    return global_addon_executor.apply_did_challenge(DidChallengeAddOnPayload.from_dict({
        "trial": Trial.from_dict({
            "seq": arg.seq,
            "name": name,
            "request_time": req_time.strftime("%Y/%m/%d %H:%M:%S.%f"),
            "status": status,
            "path": arg.req.path or "No path",
            "queries": arg.req.qs,
            "headers": arg.req.headers,
            "diff_keys": diff_keys,
            "one": {
                "url": res_one.url,
                "status_code": res_one.status_code,
                "byte": len(res_one.body),
                "response_sec": to_sec(res_one.elapsed),
                "content_type": res_one.headers.get("content-type"),
                "encoding": res_one.encoding,
                "file": file_one
            },
            "other": {
                "url": res_other.url,
                "status_code": res_other.status_code,
                "byte": len(res_other.body),
                "response_sec": to_sec(res_other.elapsed),
                "content_type": res_other.headers.get("content-type"),
                "encoding": res_other.encoding,
                "file": file_other
            }
        })
    })).trial


def exec(args: Args, config: Config, reqs: TList[Request], key: str, retry_hash: Optional[str]) -> Report:
    title = args.title.get() or config.title.get() or "No title"
    description = args.description.get() or config.description.get() or None
    logger.info(f"""
--------------------------------------------------------------------------------
| >>> Start processing !!
|
| [Key]
| {key}
|
| [Title]
| {title}
|
| [Description]
| {description}
--------------------------------------------------------------------------------
    """)

    # Provision
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))

    make_dir(f'{config.output.response_dir}/{key}/one')
    make_dir(f'{config.output.response_dir}/{key}/other')

    # Parse inputs to args of multi-thread executor.
    ex_args = TList(reqs).emap(lambda x, i: {
        "seq": i + 1,
        "number_of_request": len(reqs),
        "key": key,
        "session": s,
        "req": x,
        "host_one": config.one.host,
        "host_other": config.other.host,
        "proxy_one": Proxy.from_host(config.one.proxy),
        "proxy_other": Proxy.from_host(config.other.proxy),
        "res_dir": config.output.response_dir
    })

    # Challenge
    start_time = now()
    with futures.ThreadPoolExecutor(max_workers=args.threads.get() or config.threads) as ex:
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
        },
        "output": config.output.to_dict()
    })

    return Report.from_dict({
        "key": key,
        "title": title,
        "description": description,
        "summary": summary.to_dict(),
        "trials": trials.to_dicts(),
        "addons": config.addons.to_dict(),
        "retry_hash": retry_hash,
        "ignores": config.addons.judgement \
            .filter(_.name == 'jumeaux.addons.judgement.ignore_properties') \
            .flat_map(lambda x: x.config.map(_["ignores"]).get_or([]))
    })


def hash_from_args(args: Args) -> str:
    return hashlib.sha256((str(now()) + args.to_json()).encode()).hexdigest()


def create_config(config_paths: TList[str]) -> Config:
    def apply_include(addon: dict, config_path: str) -> dict:
        return load_yamlf(os.path.join(os.path.dirname(config_path), addon['include']), 'utf8') \
            if 'include' in addon else addon

    def apply_include_addons(addons: dict, config_path: str) -> dict:
        def apply_includes(name: str):
            return [apply_include(a, config_path) for a in addons.get(name, [])]

        return {k: v for k, v in {
            "log2reqs": apply_include(addons["log2reqs"], config_path) \
                   if "log2reqs" in addons else None,
            "reqs2reqs": apply_includes("reqs2reqs"),
            "res2res": apply_includes("res2res"),
            "res2dict": apply_includes("res2dict"),
            "judgement": apply_includes("judgement"),
            "store_criterion": apply_includes("store_criterion"),
            "dump": apply_includes("dump"),
            "did_challenge": apply_includes("did_challenge"),
            "final": apply_includes("final"),
        }.items() if v}

    def reducer(merged: dict, config_path: str) -> dict:
        d = load_yamlf(config_path, 'utf8')
        if 'addons' in d and 'addons' in merged:
            merged['addons'].update(d['addons'])
            del d['addons']
        merged.update(d)
        if 'addons' in merged:
            merged['addons'].update(apply_include_addons(merged["addons"], config_path))
        return merged

    return Config.from_dict(config_paths.reduce(reducer, {}))


def create_config_from_report(report: Report) -> Config:
    return Config.from_dict({
        "one": report.summary.one.to_dict(),
        "other": report.summary.other.to_dict(),
        "output": report.summary.output.to_dict(),
        "threads": 1,
        "title": report.title,
        "description": report.description,
        "addons": report.addons.get().to_dict()
    })


def main():
    args: Args = Args.from_dict(docopt(__doc__, version=__version__))
    global global_addon_executor
    # TODO: refactoring
    if args.retry:
        report: Report = Report.from_jsonf(args.report.get())
        config: Config = create_config_from_report(report)
        global_addon_executor = AddOnExecutor(config.addons)
        origin_logs: TList[Request] = report.trials.map(lambda x: Request.from_dict({
            'path': x.path,
            'qs': x.queries,
            'headers': x.headers,
            'name': x.name
        }))
        retry_hash: Optional[str] = report.key
    else:
        config: Config = create_config(args.config.get())
        global_addon_executor = AddOnExecutor(config.addons)
        input_paths = args.files.get() or config.input_files.get()
        origin_logs: TList[Request] = input_paths.flat_map(
            lambda f: global_addon_executor.apply_log2reqs(
                Log2ReqsAddOnPayload.from_dict({
                    'file': f
                })
            )
        )
        retry_hash: Optional[str] = None

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=config.output.encoding)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=config.output.encoding)

    # Logging settings load
    logger_config = config.output.logger.get()
    if logger_config:
        logger_config.update({'disable_existing_loggers': False})
        logging.config.dictConfig(logger_config)

    # Requests
    logs: TList[Request] = global_addon_executor.apply_reqs2reqs(Reqs2ReqsAddOnPayload.from_dict({
        'requests': origin_logs
    })).requests

    report: Report = global_addon_executor.apply_final(FinalAddOnPayload.from_dict({
        'report': exec(args, config, logs, hash_from_args(args), retry_hash),
        'output_summary': config.output
    })).report

    print(report.to_pretty_json())


if __name__ == '__main__':
    main()
