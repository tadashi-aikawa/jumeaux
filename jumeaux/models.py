# -*- coding: utf-8 -*-
from owlmixin.util import O
from typing import Optional, Any, Dict, List
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum


class Status(OwlEnum):
    SAME = "same"
    DIFFERENT = "different"
    FAILURE = "failure"


class AccessPoint(OwlMixin):
    def __init__(self, name, host, proxy=None):
        self.name: str = name
        self.host: str = host
        self.proxy: Optional[str] = proxy


class OutputSummary(OwlMixin):
    def __init__(self, response_dir='response', encoding='utf8', logger=None):
        self.response_dir: str = response_dir
        self.encoding: str = encoding
        self.logger: Optional[Any] = logger


class Addon(OwlMixin):
    def __init__(self, name, cls_name: str = 'Executor', config: dict = None):
        self.name: str = name
        self.cls_name: str = cls_name
        self.config: dict = config


class Addons(OwlMixin):
    def __init__(self, log2reqs, reqs2reqs=None, res2dict=None, judgement=None,
                 store_criterion=None, dump=None, did_challenge=None, final=None):
        self.log2reqs: Addon = Addon.from_dict(log2reqs)
        self.reqs2reqs: TList[Addon] = Addon.from_optional_dicts(reqs2reqs) or TList()
        self.res2dict: TList[Addon] = Addon.from_optional_dicts(res2dict) or TList()
        self.judgement: TList[Addon] = Addon.from_optional_dicts(judgement) or TList()
        self.store_criterion: TList[Addon] = Addon.from_optional_dicts(store_criterion) or TList()
        self.dump: TList[Addon] = Addon.from_optional_dicts(dump) or TList()
        self.did_challenge: TList[Addon] = Addon.from_optional_dicts(did_challenge) or TList()
        self.final: TList[Addon] = Addon.from_optional_dicts(final) or TList()


class Config(OwlMixin):
    def __init__(self, one, other, output, threads=1,
                 title=None, description=None, input_files=None, addons=None, base=None):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.output: OutputSummary = OutputSummary.from_dict(output)
        self.threads: int = threads
        self.title: Optional[str] = title
        self.description: Optional[str] = description
        self.input_files: Optional[TList[str]] = TList(input_files) if input_files else None
        self.addons: Optional[Addons] = Addons.from_optional_dict(addons)
        self.base: Optional[str] = base


# --------


class Args(OwlMixin):
    def __init__(self, files, title: str, description: str, config: str, threads: str, retry: bool, report: str):
        self.files: TList[str] = TList(files)
        self.title: str = title
        self.description: str = description
        self.config: str = config
        self.threads: Optional[int] = O(threads).then_or_none(int)
        self.retry: bool = retry
        self.report: str = report


class Request(OwlMixin):
    def __init__(self, path, qs=None, headers=None, name=None):
        self.path: str = path
        self.qs: TDict[TList[str]] = TDict(qs) if qs else {}
        self.headers: TDict[str] = TDict(headers) if headers else {}
        self.name: Optional[str] = name


class Proxy(OwlMixin):
    def __init__(self, http: str = None, https: str = None):
        self.http: Optional[str] = http
        self.https: Optional[str] = https

    @classmethod
    def from_host(cls, host: Optional[str]) -> 'Proxy':
        return Proxy.from_dict({
            'http': f"http://{host}",
            'https': f"https://{host}",
        }) if host else None


# --------

class ChallengeArg(OwlMixin):
    def __init__(self, seq: int, number_of_request: int, key: str, name: str,
                 session: object, host_one: str, host_other: str, path: str, res_dir: str,
                 qs: TDict[TList[str]], headers: TDict[str], proxy_one: Proxy, proxy_other: Proxy):
        self.seq: int = seq
        self.number_of_request: int = number_of_request
        self.key: str = key
        self.name: str = name
        self.session: object = session
        self.host_one: str = host_one
        self.host_other: str = host_other
        self.path: str = path
        self.res_dir: str = res_dir
        self.qs: TDict[TList[str]] = qs
        self.headers: TDict[str] = headers
        self.proxy_one: Optional[Proxy] = proxy_one
        self.proxy_other: Optional[Proxy] = proxy_other


# --------

class Report(OwlMixin):
    def __init__(self, key: str, title: str, summary: dict, trials: list,
                 addons: Addons=None, retry_hash: str=None, description: str=None):
        self.key: str = key
        self.title: str = title
        self.description: Optional[str] = description
        self.summary: Summary = Summary.from_dict(summary)
        self.trials: TList[Trial] = Trial.from_dicts(trials)
        self.addons: Optional[Addons] = Addons.from_optional_dict(addons)
        self.retry_hash: Optional[str] = retry_hash


class Summary(OwlMixin):
    def __init__(self, one: dict, other: dict, status: TDict[str], paths: TDict[str], time: dict, output: dict):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.status: StatusCounts = StatusCounts.from_dict(status)
        self.paths: TDict[str] = paths
        self.time: Time = Time.from_dict(time)
        self.output: OutputSummary = OutputSummary.from_dict(output)


class StatusCounts(OwlMixin):
    def __init__(self, same: int = 0, different: int = 0, failure: int = 0):
        self.same: int = same
        self.different: int = different
        self.failure: int = failure


class Time(OwlMixin):
    def __init__(self, start: str, end: str, elapsed_sec: int):
        self.start: str = start  # yyyy/MM/dd hh:mm:ss
        self.end: str = end  # yyyy/MM/dd hh:mm:ss
        self.elapsed_sec: int = elapsed_sec


class DiffKeys(OwlMixin):
    def __init__(self, changed: List[str], added: List[str], removed: List[str]):
        self.changed: TList[str] = TList(changed)
        self.added: TList[str] = TList(added)
        self.removed: TList[str] = TList(removed)


class Trial(OwlMixin):
    def __init__(self, seq: int, name: str, headers: dict, queries: dict, one: dict, other: dict,
                 path: str, request_time: str, status: str, diff_keys: dict=None):
        self.seq: int = seq
        self.name: str = name
        self.headers: Dict[str, str] = headers
        self.queries: Dict[str, List[str]] = queries
        self.one: ResponseSummary = ResponseSummary.from_dict(one)
        self.other: ResponseSummary = ResponseSummary.from_dict(other)
        self.path: str = path
        self.request_time: str = request_time
        self.status: Status = Status(status)
        # `None` is not same as `{}`. `{}` means no diffs, None means unknown
        self.diff_keys: Optional[DiffKeys] = DiffKeys.from_optional_dict(diff_keys)


class ResponseSummary(OwlMixin):
    def __init__(self, url: str, status_code: int = None, byte: int = None, response_sec: int = None,
                 content_type: str = None, encoding: str = None, file: Optional[str] = None):
        self.url: str = url
        self.status_code: Optional[int] = status_code
        self.byte: Optional[int] = byte
        self.response_sec: Optional[int] = response_sec
        self.content_type: Optional[str] = content_type
        self.encoding: Optional[str] = encoding
        self.file: Optional[str] = file


# ---

class Log2ReqsAddOnPayload(OwlMixin):
    def __init__(self, file: str):
        self.file: str = file


class Reqs2ReqsAddOnPayload(OwlMixin):
    def __init__(self, requests: TList[Request]):
        self.requests: TList[Request] = requests


class DumpAddOnPayload(OwlMixin):
    def __init__(self, response, body: bytes, encoding: str):
        self.response = response  # requests style
        self.body = body
        self.encoding = encoding


class Res2DictAddOnPayload(OwlMixin):
    def __init__(self, response, result: Optional[dict]):
        self.response = response  # requests style
        self.result: Optional[dict] = result


class DidChallengeAddOnPayload(OwlMixin):
    def __init__(self, trial: Trial):
        self.trial: Trial = trial


class JudgementAddOnPayload(OwlMixin):
    def __init__(self, path: str, qs: TDict[TList[str]], headers: TDict[str],
                 res_one, res_other, diff_keys: Optional[dict], regard_as_same: bool):
        self.path: str = path
        self.qs: TDict[TList[str]] = qs
        self.headers: TDict[str] = headers
        self.res_one = res_one  # requests style
        self.res_other = res_other  # requests style
        # None if unknown
        self.diff_keys: Optional[DiffKeys] = DiffKeys.from_optional_dict(diff_keys)
        self.regard_as_same: bool = regard_as_same


class StoreCriterionAddOnPayload(OwlMixin):
    def __init__(self, status: Status, path: str, qs: TDict[TList[str]], headers: TDict[str],
                 res_one, res_other, stored: bool):
        self.status: Status = status
        self.path: str = path
        self.qs: TDict[TList[str]] = qs
        self.headers: TDict[str] = headers
        self.res_one = res_one  # requests style
        self.res_other = res_other  # requests style
        self.stored: bool = stored


class FinalAddOnPayload(OwlMixin):
    def __init__(self, report: Report, output_summary: OutputSummary):
        self.report: Report = report
        self.output_summary: OutputSummary = output_summary
