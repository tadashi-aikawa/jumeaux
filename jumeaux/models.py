# -*- coding: utf-8 -*-
import datetime
from typing import Optional, Any, Dict, List
from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum
from requests.structures import CaseInsensitiveDict as RequestsCaseInsensitiveDict


class CaseInsensitiveDict(RequestsCaseInsensitiveDict):
    pass


class Status(OwlEnum):
    SAME = "same"
    DIFFERENT = "different"
    FAILURE = "failure"


class AccessPoint(OwlMixin):
    name: str
    host: str
    proxy: TOption[str]


class OutputSummary(OwlMixin):
    response_dir: str = 'response'
    encoding: str = 'utf8'
    logger: TOption[any]


class Addon(OwlMixin):
    name: str
    cls_name: str = 'Executor'
    config: TOption[dict]
    include: TOption[str]


# List is None...
class Addons(OwlMixin):
    log2reqs: Addon
    reqs2reqs: TList[Addon] = []
    res2res: TList[Addon] = []
    res2dict: TList[Addon] = []
    judgement: TList[Addon] = []
    store_criterion: TList[Addon] = []
    dump: TList[Addon] = []
    did_challenge: TList[Addon] = []
    final: TList[Addon] = []


class Config(OwlMixin):
    one: AccessPoint
    other: AccessPoint
    output: OutputSummary
    threads: int = 1
    title: TOption[str]
    description: TOption[str]
    input_files: TOption[TList[str]]
    addons: Addons


# --------


class Args(OwlMixin):
    files: TOption[TList[str]]
    title: TOption[str]
    description: TOption[str]
    config: TOption[TList[str]]
    threads: TOption[int]
    retry: bool
    report: TOption[str]  # Only case in which retry is True

    @classmethod
    def ___threads(cls, v: Optional[str]) -> int:
        return int(v) if v else None


# or {}
class Request(OwlMixin):
    name: TOption[str]
    path: str
    qs: TDict[TList[str]] = {}
    headers: TDict[str] = {}


class Proxy(OwlMixin):
    http: str = None
    https: str = None

    @classmethod
    def from_host(cls, host: TOption[str]) -> 'Proxy':
        return Proxy.from_dict({
            'http': f"http://{host.get()}",
            'https': f"https://{host.get()}",
        }) if not host.is_none() else None


class Response(OwlMixin):
    body: bytes
    encoding: TOption[str]
    text: str
    headers: CaseInsensitiveDict
    url: str
    status_code: int
    elapsed: datetime.timedelta

    @classmethod
    def ___headers(cls, v):
        return CaseInsensitiveDict(v)

    @classmethod
    def from_requests(cls, res: any) -> 'Response':
        return Response.from_dict({
            'body': res.content,
            'encoding': res.encoding,
            'text': res.text,
            'headers': res.headers,
            'url': res.url,
            'status_code': res.status_code,
            'elapsed': res.elapsed,
        })


# --------

class ChallengeArg(OwlMixin):
    seq: int
    number_of_request: int
    key: str
    session: object
    req: Request
    host_one: str
    host_other: str
    proxy_one: TOption[Proxy]
    proxy_other: TOption[Proxy]
    res_dir: str

# --------


class StatusCounts(OwlMixin):
    same: int = 0
    different: int = 0
    failure: int = 0


class Time(OwlMixin):
    start: str  # yyyy/MM/dd hh:mm:ss
    end: str  # yyyy/MM/dd hh:mm:ss
    elapsed_sec: int


class Summary(OwlMixin):
    one: AccessPoint
    other: AccessPoint
    status: StatusCounts
    paths: TDict[int]
    time: Time
    output: OutputSummary


class DiffKeys(OwlMixin):
    added: TList[str]
    changed: TList[str]
    removed: TList[str]


class ResponseSummary(OwlMixin):
    url: str
    status_code: TOption[int]
    byte: TOption[int]
    response_sec: TOption[float]
    content_type: TOption[str]
    encoding: TOption[str]
    file: TOption[str]


class Condition(OwlMixin):
    name: TOption[str]
    path: TOption[str]
    added: TList[str] = []
    removed: TList[str] = []
    changed: TList[str] = []


class Ignore(OwlMixin):
    title: str
    conditions: TList[Condition]
    image: TOption[str]
    link: TOption[str]


class Trial(OwlMixin):
    seq: int
    name: str
    headers: TDict[str]
    queries: TDict[TList[str]]
    one: ResponseSummary
    other: ResponseSummary
    path: str
    request_time: str
    status: Status
    # `None` is not same as `{}`. `{}` means no diffs, None means unknown
    diff_keys: TOption[DiffKeys]


class Report(OwlMixin):
    key: str
    title: str
    description: TOption[str]
    summary: Summary
    trials: TList[Trial]
    addons: TOption[Addons]
    retry_hash: TOption[str]
    ignores: TList[Ignore] = []

# ---


class Log2ReqsAddOnPayload(OwlMixin):
    file: str


class Reqs2ReqsAddOnPayload(OwlMixin):
    requests: TList[Request]


class DumpAddOnPayload(OwlMixin):
    response: Response
    body: bytes
    encoding: TOption[str]


class Res2ResAddOnPayload(OwlMixin):
    response: Response
    req: Request


class Res2DictAddOnPayload(OwlMixin):
    response: Response
    result: TOption[dict]


class DidChallengeAddOnPayload(OwlMixin):
    trial: Trial


class JudgementAddOnPayload(OwlMixin):
    name: str
    path: str
    qs: TDict[TList[str]]
    headers: TDict[str]
    res_one: Response
    res_other: Response
    # None if unknown
    diff_keys: TOption[DiffKeys]
    remaining_diff_keys: TOption[DiffKeys]
    regard_as_same: bool


class StoreCriterionAddOnPayload(OwlMixin):
    status: Status
    path: str
    qs: TDict[TList[str]]
    headers: TDict[str]
    res_one: Response
    res_other: Response
    stored: bool


class FinalAddOnPayload(OwlMixin):
    report: Report
    output_summary: OutputSummary
