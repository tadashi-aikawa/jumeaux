#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import io
import os
import re
import sys
import urllib.parse as urlparser
from concurrent import futures
from typing import Tuple, Optional, Any

import requests
from deepdiff import DeepDiff
from fn import _
from owlmixin import TList, TOption, TDict
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(PROJECT_ROOT)
# sys.path.append(os.getcwd())
from jumeaux import __version__
from jumeaux.addons import AddOnExecutor
from jumeaux.utils import to_jumeaux_xpath, mill_seconds_until, now, parse_datetime_dsl
from jumeaux.domain.config.service import (
    create_config_from_report,
    create_config,
    merge_args2config,
)
from jumeaux.domain.config.vo import Config, MergedArgs

# XXX: ...
from jumeaux.logger import Logger
from jumeaux.models import (
    to_json,
    Report,
    Request,
    Response,
    ChallengeArg,
    Trial,
    Proxy,
    Summary,
    Concurrency,
    Log2ReqsAddOnPayload,
    Reqs2ReqsAddOnPayload,
    Res2ResAddOnPayload,
    Res2DictAddOnPayload,
    JudgementAddOnPayload,
    JudgementAddOnReference,
    StoreCriterionAddOnPayload,
    StoreCriterionAddOnReference,
    DumpAddOnPayload,
    FinalAddOnPayload,
    DidChallengeAddOnPayload,
    DidChallengeAddOnReference,
    DiffKeys,
    Status,
    DictOrList,
    QueryCustomization,
    FinalAddOnReference,
    HttpMethod,
)

logger: Logger = Logger(__name__)
global_addon_executor: AddOnExecutor

START_JUMEAUX_AA = r"""
        ____  _             _         _
__/\__ / ___|| |_ __ _ _ __| |_      | |_   _ _ __ ___   ___  __ _ _   ___  __ __/\__
\    / \___ \| __/ _` | '__| __|  _  | | | | | '_ ` _ \ / _ \/ _` | | | \ \/ / \    /
/_  _\  ___) | || (_| | |  | |_  | |_| | |_| | | | | | |  __/ (_| | |_| |>  <  /_  _\
  \/   |____/ \__\__,_|_|   \__|  \___/ \__,_|_| |_| |_|\___|\__,_|\__,_/_/\_\   \/


                    ..JgHggggggggHm&..   ...gWggggggggggHa-..
                .(WgggggggggggggggggggNNNMgggggggggggggggggggHa,
             .(ggggggggggggggggggggMMMMMMMMNggggggggggggggggggggga,
           .dggggggggggggggggggggHMMMMMMMMMMMNgggggggggggggggggggggN,
        ..ggggggggggggggggggggg@NMMMMMMMMMMMMMNHgggggggggggggggggggggHa.   `
      .JgggggggggggggggggggggggNMMMMMMMMMMMMMMMMHgggggggggggggggggggggggn.
     .ggggggggggggggggggggggggNMMMMMMMMMMMMMMMMMMggggggggggggggggggggggggH,
   .dgggggggggggggggggggggggg@MMMMMMMMMMMMMMMMMMMNgggggggggggggggggggggggggh.
  .ggggggggggggggggggggggggggMMMMMMMMMMMMMMMMMMMMMggggggggggggggggggggggggggH,
 .gggggggggggggggggggggggggggMMMMMMMMMMMMMMMMMMMMMNg@ggggggggggggggggggggggggH,
 dggggggggggggggggggggggggg@gMMMMMMMMMMMMMMMMMMMMMNgggggggggggggggggggggggggggL
 WgggggggggggggggggggggggggggMMMMMMMMMMMMMMMMMMMMMMgggggggggggggggggggggggggggP
 (gggggggggggggggggggggggggggMMMMMMMMMMMMMMMMMMMMMMggggggggggggggggggggggggggH'
  ,UggggggggggggggggggggggggggMMMMMMMMMMMMMMMMMMMMgggggggggggggggggggggggggHY`
     ?"YHgHHBHHgggggggggggggggMMMMMMMMMMMMMMMMMMMNggggggggggggggHWYWHgHY""(
    JH.      _?!~-?"4HggggggggMMMMMMMMMMMMMMMMMMMHgggggggg#"=~`~!`       .gL
   .ggh               (HgggggggMMMMMMMMMMMMMMMMMNgggggggf`              .Hgg,
   JggH                ,HYJggggMMMMMMMMMMMMMMMMMMgggg]7g|               .ggg]
   dggF               ."` HggggHMMMMMMMMMMMMMMMMgggggb  7.               Ogg]
   JgK                   .ggggggMMMMMMMMMMMMMMMNgggggH                    Hg%
   ,gHJ..                .ggggggMMMMMMMMMMMMMMMNgggggH                 ..(gg:
    ggggg\                ggggggMMMMMMMMMMMMMMMMgggggK                (ggggK
    zgggH,                4@ggg@MMMMMMMMMMMMMMMNgggggF             Ta..gggg%
    .ggggH,               ,gggggMMMMMMMMMMMMMMMNggggg!               (ggggH
     jWggggL        ..,    WgggMMMMMMMMMMMMMMMMMNgggP    .J,       .dggggD%
     ./Hggggh.   ..WggH.   .HNMMMMMMMMMMMMMMMMMMMNH@    .gggH&, ` .Wgggg@,
      G(gggggg@ggggggggh..+udMMMMMMMMMMMMMMMMMMMMMMmZ>-.Hggggggggggggggg%]
      ,(ggggggggggggggggMggggHMMMMMMMMMMMMMMMMMMMMgggggMgggggggggggggggg({
      .wggggggggggggggggg,7HgggMMMMMMMMMMMMMMMMMMgggHY(gggggggggggggggggJ`
      .Wggggggggggggggggg]    ???jMMMMMMMMMMM#?777!   JgggggggggggggggggW<
     .XggggggggggggggggggP      _?""Y"'"HHBYY""!      Wggggggggggggggggggh
    .JgggggggggggggggggggP                            WggggggggggggggggggHJ.
...dggggggggggggggggggggg]                            q@ggggggggggggggggggggm-..
  _7""Y""!.gggggggggggggH`                            .gggggggggggggg;_""Y""'!
         .WggggggggggggH^                              (gggggggggggggh
        .dggggggggggggB!                                ,Hggggggggggggh
       .dggggggggggg#=                                    ?Hgggggggggggh.
      .gggggggggg#"!                                        -THgggggggggH,
    .dgggggHYY"!                                                ?"YWHgggggh,

"""

CONFIG_AA = r"""
         ____             __ _
__/\__  / ___|___  _ __  / _(_) __ _  __/\__
\    / | |   / _ \| '_ \| |_| |/ _` | \    /
/_  _\ | |__| (_) | | | |  _| | (_| | /_  _\\
  \/    \____\___/|_| |_|_| |_|\__, |   \/
                               |___/
"""


def write_to_file(name, dir, body):
    with open(f"{dir}/{name}", "wb") as f:
        f.write(body)


def make_dir(path):
    os.makedirs(path)
    os.chmod(path, 0o777)


def http_get(args: Tuple[Any, str, TDict[str], TOption[Proxy]]):
    session, url, headers, proxies = args
    try:
        r = session.get(url, headers=headers, proxies=proxies.map(lambda x: x.to_dict()).get_or({}))
    finally:
        session.close()
    return r


def http_post(
    args: Tuple[Any, str, TOption[str], TOption[dict], TOption[dict], TDict[str], TOption[Proxy]]
):
    session, url, raw, form, json_, headers, proxies = args
    try:
        r = session.post(
            url,
            data=raw.get() or form.get(),
            json=json_.get(),
            headers=headers,
            proxies=proxies.map(lambda x: x.to_dict()).get_or({}),
        )
    finally:
        session.close()
    return r


def merge_headers(access_point_base: TDict[str], this_request: TDict[str]) -> TDict[str]:
    return (
        TDict({"User-Agent": f"jumeaux/{__version__}"})
        .assign(access_point_base)
        .assign(this_request)
    )


def concurrent_request(
    session,
    *,
    headers: TDict[str],
    method: HttpMethod,
    raw: TOption[str],
    form: TOption[dict],
    json_: TOption[dict],
    url_one: str,
    url_other: str,
    headers_one: TDict[str],
    headers_other: TDict[str],
    proxies_one: TOption[Proxy],
    proxies_other: TOption[Proxy],
):
    merged_header_one: TDict[str] = merge_headers(headers_one, headers)
    merged_header_other: TDict[str] = merge_headers(headers_other, headers)
    logger.debug(f"One   Request headers: {merged_header_one}")
    logger.debug(f"Other Request headers: {merged_header_other}")

    with futures.ThreadPoolExecutor(max_workers=2) as ex:
        if method is HttpMethod.GET:
            res_one, res_other = ex.map(
                http_get,
                (
                    (session, url_one, merged_header_one, proxies_one),
                    (session, url_other, merged_header_other, proxies_other),
                ),
            )
        elif method is HttpMethod.POST:
            res_one, res_other = ex.map(
                http_post,
                (
                    (session, url_one, raw, form, json_, merged_header_one, proxies_one),
                    (session, url_other, raw, form, json_, merged_header_other, proxies_other),
                ),
            )
        else:
            # Unreachable
            raise RuntimeError

    return res_one, res_other


def res2res(res: Response, req: Request) -> Res2ResAddOnPayload:
    return global_addon_executor.apply_res2res(
        Res2ResAddOnPayload.from_dict({"response": res, "req": req, "tags": []})
    )


def res2dict(res: Response) -> TOption[dict]:
    return global_addon_executor.apply_res2dict(
        Res2DictAddOnPayload.from_dict({"response": res, "result": None})
    ).result


def judgement(
    r_one: Response,
    r_other: Response,
    d_one: TOption[DictOrList],
    d_other: TOption[DictOrList],
    name: str,
    path: str,
    qs: TDict[TList[str]],
    headers: TDict[str],
    diffs_by_cognition: Optional[TDict[DiffKeys]],
) -> Tuple[Status, TOption[TDict[DiffKeys]]]:
    result: JudgementAddOnPayload = global_addon_executor.apply_judgement(
        JudgementAddOnPayload.from_dict(
            {
                "diffs_by_cognition": diffs_by_cognition
                and diffs_by_cognition.omit_by(lambda k, v: v.is_empty()),
                "regard_as_same": r_one.body == r_other.body
                if diffs_by_cognition is None
                else diffs_by_cognition["unknown"].is_empty(),
            }
        ),
        JudgementAddOnReference.from_dict(
            {
                "name": name,
                "path": path,
                "qs": qs,
                "headers": headers,
                "dict_one": d_one,
                "dict_other": d_other,
                "res_one": r_one,
                "res_other": r_other,
            }
        ),
    )

    status: Status = Status.SAME if result.regard_as_same else Status.DIFFERENT  # type: ignore # Prevent for enum problem

    return status, result.diffs_by_cognition


def store_criterion(status: Status, name: str, req: Request, r_one: Response, r_other: Response):
    return global_addon_executor.apply_store_criterion(
        StoreCriterionAddOnPayload.from_dict({"stored": False}),
        StoreCriterionAddOnReference.from_dict(
            {
                "status": status,
                "req": {"name": name, "path": req.path, "qs": req.qs, "headers": req.headers},
                "res_one": r_one,
                "res_other": r_other,
            }
        ),
    ).stored


def dump(res: Response):
    return global_addon_executor.apply_dump(
        DumpAddOnPayload.from_dict({"response": res, "body": res.body, "encoding": res.encoding})
    ).body


def to_sec(elapsed):
    return round(elapsed.seconds + elapsed.microseconds / 1000000, 2)


def select_key_as_case_insensitive(target_key_pattern: str, qs: TDict[TList[str]]) -> str:
    case_insensitive: bool = target_key_pattern.endswith("/i")
    target_key = target_key_pattern[:-2] if case_insensitive else target_key_pattern

    def matcher(x):
        return x.lower() == target_key.lower() if case_insensitive else x == target_key

    return TList(qs.keys()).find(matcher).get_or(target_key)


def create_query_string(
    qs: TDict[TList[str]], cqs: TOption[QueryCustomization], encoding: str
) -> str:
    if cqs.is_none():
        return urlparser.urlencode(qs, doseq=True, encoding=encoding)

    overwritten = qs.assign(
        {
            select_key_as_case_insensitive(k, qs): [parse_datetime_dsl(v) for v in vs]
            for k, vs in cqs.get().overwrite.get_or(TDict()).to_dict().items()
        }
    )
    removed = {
        k: v
        for k, v in overwritten.items()
        if k
        not in [select_key_as_case_insensitive(x, qs) for x in cqs.get().remove.get_or(TList())]
    }

    return urlparser.urlencode(removed, doseq=True, encoding=encoding)


def challenge(arg_dict: dict) -> dict:
    """
    [[[ WARNING !!!!! ]]]
    `arg_dict` is dict like `ChallengeArg` because HttpMethod(OwlEnum) can't be pickled.
    Return value is dict like `Trial` because Status(OwlEnum) can't be pickled.
    """
    arg: ChallengeArg = ChallengeArg.from_dict(arg_dict)

    name: str = arg.req.name.get_or(str(arg.seq))
    log_prefix = f"[{arg.seq} / {arg.number_of_request}]"

    logger.info_lv3(f"{log_prefix} {'-'*80}")
    logger.info_lv3(f"{log_prefix}  {arg.seq}. {arg.req.name.get_or(arg.req.path)}")
    logger.info_lv3(f"{log_prefix} {'-'*80}")

    path_str_one = arg.path_one.map(lambda x: re.sub(x.before, x.after, arg.req.path)).get_or(
        arg.req.path
    )
    path_str_other = arg.path_other.map(lambda x: re.sub(x.before, x.after, arg.req.path)).get_or(
        arg.req.path
    )
    qs_str_one = create_query_string(arg.req.qs, arg.query_one, arg.req.url_encoding)
    qs_str_other = create_query_string(arg.req.qs, arg.query_other, arg.req.url_encoding)
    url_one = f"{arg.host_one}{path_str_one}?{qs_str_one}"
    url_other = f"{arg.host_other}{path_str_other}?{qs_str_other}"

    # Get two responses
    req_time = now()
    try:
        logger.info_lv3(f"{log_prefix} One   URL:   {url_one}")
        logger.debug(f"{log_prefix} One   PROXY: {arg.proxy_one.map(lambda x: x.to_dict()).get()}")

        logger.info_lv3(f"{log_prefix} Other URL:   {url_other}")
        logger.debug(
            f"{log_prefix} Other PROXY: {arg.proxy_other.map(lambda x: x.to_dict()).get()}"
        )

        if arg.req.headers:
            logger.info_lv3(f"{log_prefix} Additional headers:   {arg.req.headers}")
        if arg.req.raw.any():
            logger.info_lv3(f"{log_prefix} raw:   {arg.req.raw.get()}")
        if arg.req.form.any():
            logger.info_lv3(f"{log_prefix} form:   {arg.req.form.get()}")
        if arg.req.json.any():
            logger.info_lv3(f"{log_prefix} json:   {arg.req.json.get()}")

        r_one, r_other = concurrent_request(
            arg.session,
            headers=arg.req.headers,
            method=arg.req.method,
            raw=arg.req.raw,
            form=arg.req.form,
            json_=arg.req.json,
            url_one=url_one,
            url_other=url_other,
            headers_one=arg.headers_one,
            headers_other=arg.headers_other,
            proxies_one=arg.proxy_one,
            proxies_other=arg.proxy_other,
        )

        logger.info_lv3(
            f"{log_prefix} One:   {r_one.status_code} / {to_sec(r_one.elapsed)}s / {len(r_one.content)}b / {r_one.headers.get('content-type')}"  # noqa
        )
        logger.info_lv3(
            f"{log_prefix} Other: {r_other.status_code} / {to_sec(r_other.elapsed)}s / {len(r_other.content)}b / {r_other.headers.get('content-type')}"  # noqa
        )
    except ConnectionError:
        logger.info_lv1(f"{log_prefix} 💀 {arg.req.name.get()}")
        # TODO: Integrate logic into create_trial
        return Trial.from_dict(
            {
                "seq": arg.seq,
                "name": name,
                "tags": [],
                "request_time": req_time.isoformat(),
                "status": "failure",
                "method": arg.req.method,
                "path": arg.req.path,
                "queries": arg.req.qs,
                "raw": arg.req.raw,
                "form": arg.req.form,
                "json": arg.req.json,
                "headers": arg.req.headers,
                "one": {"url": url_one, "type": "unknown"},
                "other": {"url": url_other, "type": "unknown"},
            }
        ).to_dict()

    res2res_one_begin = now()
    res_one_payload: Res2ResAddOnPayload = res2res(
        Response.from_requests(r_one, arg.default_response_encoding_one), arg.req
    )
    res_one = res_one_payload.response
    logger.info_lv3(f"{log_prefix} ⏰ One   res2res:   {mill_seconds_until(res2res_one_begin)}ms")

    res2res_other_begin = now()
    res_other_payload: Res2ResAddOnPayload = res2res(
        Response.from_requests(r_other, arg.default_response_encoding_other), arg.req
    )
    res_other = res_other_payload.response
    logger.info_lv3(
        f"{log_prefix} ⏰ Other   res2res:   {mill_seconds_until(res2res_other_begin)}ms"
    )

    res2dict_one_begin = now()
    dict_one: TOption[DictOrList] = res2dict(res_one)
    logger.info_lv3(f"{log_prefix} ⏰ One   res2dict:   {mill_seconds_until(res2dict_one_begin)}ms")

    res2dict_other_begin = now()
    dict_other: TOption[DictOrList] = res2dict(res_other)
    logger.info_lv3(
        f"{log_prefix} ⏰ Other   res2dict:   {mill_seconds_until(res2dict_other_begin)}ms"
    )

    # Create diff
    # Either dict_one or dic_other is None, it means that it can't be analyzed, therefore return None
    diff_diagnosis_begin = now()
    ddiff = (
        None
        if dict_one.is_none() or dict_other.is_none()
        else {}
        if res_one.body == res_other.body
        else DeepDiff(dict_one.get(), dict_other.get())
    )
    logger.info_lv3(
        f"{log_prefix} ⏰ Diff diagnosis:   {mill_seconds_until(diff_diagnosis_begin)}ms"
    )

    initial_diffs_by_cognition: Optional[TDict[DiffKeys]] = TDict(
        {
            "unknown": DiffKeys.from_dict(
                {
                    "changed": TList(
                        ddiff.get("type_changes", {}).keys()
                        | ddiff.get("values_changed", {}).keys()
                    )
                    .map(to_jumeaux_xpath)
                    .order_by(_),
                    "added": TList(
                        ddiff.get("dictionary_item_added", {})
                        | ddiff.get("iterable_item_added", {}).keys()
                    )
                    .map(to_jumeaux_xpath)
                    .order_by(_),
                    "removed": TList(
                        ddiff.get("dictionary_item_removed", {})
                        | ddiff.get("iterable_item_removed", {}).keys()
                    )
                    .map(to_jumeaux_xpath)
                    .order_by(_),
                }
            )
        }
    ) if ddiff is not None else None

    # Judgement
    judgement_begin = now()
    status, diffs_by_cognition = judgement(
        res_one,
        res_other,
        dict_one,
        dict_other,
        name,
        arg.req.path,
        arg.req.qs,
        arg.req.headers,
        initial_diffs_by_cognition,
    )
    logger.info_lv3(f"{log_prefix} ⏰ Judgement:   {mill_seconds_until(judgement_begin)}ms")

    status_symbol = "O" if status == Status.SAME else "X"
    log_msg = f"{log_prefix} {status_symbol} ({res_one.status_code} - {res_other.status_code}) <{res_one.elapsed_sec}s - {res_other.elapsed_sec}s> {{{arg.req.method}}} {arg.req.name.get_or(arg.req.path)}"  # noqa
    (logger.info_lv2 if status == Status.SAME else logger.info_lv1)(log_msg)

    # Store files
    store_criterion_begin = now()
    file_one: Optional[str] = None
    file_other: Optional[str] = None
    prop_file_one: Optional[str] = None
    prop_file_other: Optional[str] = None
    if store_criterion(status, name, arg.req, res_one, res_other):
        dir = f"{arg.res_dir}/{arg.key}"
        file_one = f"one/({arg.seq}){name}"
        file_other = f"other/({arg.seq}){name}"
        write_to_file(file_one, dir, dump(res_one))
        write_to_file(file_other, dir, dump(res_other))
        if not dict_one.is_none():
            prop_file_one = f"one-props/({arg.seq}){name}.json"
            write_to_file(
                prop_file_one, dir, to_json(dict_one.get()).encode("utf-8", errors="replace")
            )
        if not dict_other.is_none():
            prop_file_other = f"other-props/({arg.seq}){name}.json"
            write_to_file(
                prop_file_other, dir, to_json(dict_other.get()).encode("utf-8", errors="replace")
            )
    logger.info_lv3(
        f"{log_prefix} ⏰ Store criterion:   {mill_seconds_until(store_criterion_begin)}ms"
    )

    # Did challenge
    did_challenge_begin = now()
    payload = global_addon_executor.apply_did_challenge(
        DidChallengeAddOnPayload.from_dict(
            {
                "trial": Trial.from_dict(
                    {
                        "seq": arg.seq,
                        "name": name,
                        "tags": res_one_payload.tags.concat(
                            res_other_payload.tags
                        ).uniq(),  # TODO: tags created by reqs2reqs
                        "request_time": req_time.isoformat(),
                        "status": status,
                        "method": arg.req.method,
                        "path": arg.req.path,
                        "queries": arg.req.qs,
                        "raw": arg.req.raw,
                        "form": arg.req.form,
                        "json": arg.req.json,
                        "headers": arg.req.headers,
                        "diffs_by_cognition": diffs_by_cognition,
                        "one": {
                            "url": res_one.url,
                            "type": res_one.type,
                            "status_code": res_one.status_code,
                            "byte": res_one.byte,
                            "response_sec": res_one.elapsed_sec,
                            "content_type": res_one.content_type,
                            "mime_type": res_one.mime_type,
                            "encoding": res_one.encoding,
                            "file": file_one,
                            "prop_file": prop_file_one,
                        },
                        "other": {
                            "url": res_other.url,
                            "type": res_other.type,
                            "status_code": res_other.status_code,
                            "byte": res_other.byte,
                            "response_sec": res_other.elapsed_sec,
                            "content_type": res_other.content_type,
                            "mime_type": res_other.mime_type,
                            "encoding": res_other.encoding,
                            "file": file_other,
                            "prop_file": prop_file_other,
                        },
                    }
                )
            }
        ),
        DidChallengeAddOnReference.from_dict(
            {
                "res_one": res_one,
                "res_other": res_other,
                "res_one_props": dict_one,
                "res_other_props": dict_other,
            }
        ),
    )
    logger.info_lv3(f"{log_prefix} ⏰ Did challenge:   {mill_seconds_until(did_challenge_begin)}ms")

    return payload.trial.to_dict()


def create_concurrent_executor(config: Config) -> Tuple[Any, Concurrency]:
    processes = config.processes.get()
    if processes:
        return (
            futures.ProcessPoolExecutor(max_workers=processes),
            Concurrency.from_dict({"processes": processes, "threads": 1}),
        )

    threads = config.threads
    return (
        futures.ThreadPoolExecutor(max_workers=threads),
        Concurrency.from_dict({"processes": 1, "threads": threads}),
    )


def exec(config: Config, reqs: TList[Request], key: str, retry_hash: Optional[str]) -> Report:
    # Provision
    s = requests.Session()
    s.mount("http://", HTTPAdapter(max_retries=config.max_retries))
    s.mount("https://", HTTPAdapter(max_retries=config.max_retries))

    make_dir(f"{config.output.response_dir}/{key}/one")
    make_dir(f"{config.output.response_dir}/{key}/other")
    make_dir(f"{config.output.response_dir}/{key}/one-props")
    make_dir(f"{config.output.response_dir}/{key}/other-props")

    # Parse inputs to args of multi-thread executor.
    ex_args = reqs.emap(
        lambda x, i: {
            "seq": i + 1,
            "number_of_request": len(reqs),
            "key": key,
            "session": s,
            "req": x,
            "host_one": config.one.host,
            "host_other": config.other.host,
            "proxy_one": Proxy.from_host(config.one.proxy),
            "proxy_other": Proxy.from_host(config.other.proxy),
            "path_one": config.one.path,
            "path_other": config.other.path,
            "query_one": config.one.query,
            "query_other": config.other.query,
            "headers_one": config.one.headers,
            "headers_other": config.other.headers,
            "default_response_encoding_one": config.one.default_response_encoding,
            "default_response_encoding_other": config.other.default_response_encoding,
            "res_dir": config.output.response_dir,
        }
    ).to_dicts()

    # Challenge
    title = config.title.get_or("No title")
    description = config.description.get()
    tags = config.tags.get_or([])
    executor, concurrency = create_concurrent_executor(config)

    logger.info_lv1(
        f"""
--------------------------------------------------------------------------------
| {title}
| ({key})
--------------------------------------------------------------------------------
| {description}
--------------------------------------------------------------------------------
| - {concurrency.processes} processes
| - {concurrency.threads} threads
--------------------------------------------------------------------------------
    """
    )

    start_time = now()
    with executor as ex:
        trials = TList([r for r in ex.map(challenge, ex_args)]).map(Trial.from_dict)
    end_time = now()

    latest = f"{config.output.response_dir}/latest"
    if os.path.lexists(latest):
        os.remove(latest)
    os.symlink(key, latest, True)

    summary = Summary.from_dict(
        {
            "one": {
                "name": config.one.name,
                "host": config.one.host,
                "path": config.one.path,
                "query": config.one.query,
                "proxy": config.one.proxy,
                "headers": config.one.headers,
                "default_response_encoding": config.one.default_response_encoding,
            },
            "other": {
                "name": config.other.name,
                "host": config.other.host,
                "path": config.other.path,
                "query": config.other.query,
                "proxy": config.other.proxy,
                "headers": config.other.headers,
                "default_response_encoding": config.other.default_response_encoding,
            },
            "status": trials.group_by(_.status.value).map_values(len).to_dict(),
            "tags": tags,
            "time": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "elapsed_sec": (end_time - start_time).seconds,
            },
            "output": config.output.to_dict(),
            "concurrency": concurrency,
        }
    )

    return Report.from_dict(
        {
            "version": __version__,
            "key": key,
            "title": title,
            "description": description,
            "notifiers": config.notifiers,
            "summary": summary.to_dict(),
            "trials": trials.to_dicts(),
            "addons": config.addons.to_dict(),
            "retry_hash": retry_hash,
        }
    )


def __run(
    config: Config,
    origin_reqs: TList[Request],
    addon_executor: AddOnExecutor,
    hash: str,
    retry_hash: Optional[str],
):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=config.output.encoding)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=config.output.encoding)

    logger.info_lv1(START_JUMEAUX_AA)
    logger.info_lv1(f"Version: {__version__}")

    if config.output.logger.get():
        logger.warning("`output.logger` is no longer works.")
        logger.warning(
            "And this will be removed soon! You need to remove this property not to stop!"
        )

    logger.info_lv2(CONFIG_AA)
    logger.info_lv2("Merge with yaml files or report, and args")
    logger.info_lv2("----")
    logger.info_lv2(config.to_yaml())

    # XXX: Please fix to not use global!
    global global_addon_executor
    global_addon_executor = addon_executor

    # Requests
    reqs: TList[Request] = addon_executor.apply_reqs2reqs(
        Reqs2ReqsAddOnPayload.from_dict({"requests": origin_reqs}), config
    ).requests

    # Execute
    report = exec(config, reqs, hash, retry_hash)

    # Finalize
    addon_executor.apply_final(
        FinalAddOnPayload.from_dict({"report": report, "output_summary": config.output}),
        FinalAddOnReference.from_dict({"notifiers": config.notifiers}),
    )


def hash_from_args(args_str: str) -> str:
    return hashlib.sha256((str(now()) + args_str).encode()).hexdigest()


def retry(*, args: MergedArgs, report: str):
    report: Report = Report.from_jsonf(report, force_cast=True)
    config: Config = merge_args2config(args, create_config_from_report(report))
    addon_executor = AddOnExecutor(config.addons)
    origin_reqs: TList[Request] = report.trials.map(
        lambda x: Request.from_dict(
            {
                "path": x.path,
                "qs": x.queries,
                "headers": x.headers,
                "name": x.name,
                "method": x.method,
                "form": x.form,
                "json": x.json,
            }
        )
    )
    __run(config, origin_reqs, addon_executor, hash_from_args(args.to_json()), report.key)


def run(
    *, args: MergedArgs, config_paths: TList[str], skip_addon_tag: TOption[TList[str]],
):
    config: Config = merge_args2config(
        args, create_config(config_paths, skip_addon_tag),
    )

    addon_executor = AddOnExecutor(config.addons)
    origin_reqs: TList[Request] = config.input_files.get().flat_map(
        lambda f: addon_executor.apply_log2reqs(Log2ReqsAddOnPayload.from_dict({"file": f}))
    )
    __run(config, origin_reqs, addon_executor, hash_from_args(args.to_json()), None)
