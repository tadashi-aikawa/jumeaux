# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict
from modules.requestcreator import *
from enum import Enum


class Format(Enum):
    PLAIN = "plain"
    APACHE = "apache"
    YAML = "yaml"
    CSV = "csv"


class Status(Enum):
    SAME = "same"
    SAME_WITHOUT_ORDER = "same_without_order"
    DIFFERENT = "different"


class AccessPoint(OwlMixin):
    def __init__(self, name, host, proxy=None):
        self.name: str = name
        self.host: str = host
        self.proxy: Optional[str] = proxy


class InputSummary(OwlMixin):
    def __init__(self, format='plain', encoding='utf8'):
        self.format: Format = Format(format)
        self.encoding: str = encoding


class OutputSummary(OwlMixin):
    def __init__(self, response_dir='response', encoding='utf8', logger=None):
        self.response_dir: str = response_dir
        self.encoding: str = encoding
        self.logger: Optional[Any] = logger


class Config(OwlMixin):
    def __init__(self, one, other, input, output):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.input: InputSummary = InputSummary.from_dict(input)
        self.output: OutputSummary = OutputSummary.from_dict(output)


class Args(OwlMixin):
    def __init__(self, files, config: str, threads):
        self.files: TList[str] = TList(files)
        self.config: Config = Config.from_jsonf(config)
        self.threads: int = int(threads)


class Request(OwlMixin):
    def __init__(self, path, qs=None, headers=None):
        self.path = path  # type: str
        self.qs = TDict(qs) if qs else {}  # type: TDict[TList[str]]
        self.headers = TDict(headers) if headers else {}  # type: TDict[str]


class Proxy(OwlMixin):
    def __init__(self, http: str = None, https: str = None):
        self.http: Optional[str] = http
        self.https: Optional[str] = https

    @classmethod
    def from_host(cls, host: Optional[str]) -> 'Proxy':
        return Proxy.from_dict({
            'http': f"http://{host}",
            'https': f"https://{host}",
        }) if host else {}


# --------

class Report(OwlMixin):
    def __init__(self, key: str, title: str, summary: dict, trials: list):
        self.key: str = key
        self.title: str = title
        self.summary: Summary = Summary.from_dict(summary)
        self.trials: TList[Trial] = Trial.from_dicts(trials)


class Summary(OwlMixin):
    def __init__(self, one: dict, other: dict, status: dict, time: dict):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.status: Dict[Status, int] = {Status(name): num for name, num in status}
        self.time: Time = Time.from_dict(time)


class Time(OwlMixin):
    def __init__(self, start: str, end: str, elapsed_sec: int):
        self.start: str = start  # yyyy/MM/dd hh:mm:ss
        self.end: str = end    # yyyy/MM/dd hh:mm:ss
        self.elapsed_sec: int = elapsed_sec


class Trial(OwlMixin):
    def __init__(self, headers: dict, queries: dict, one: dict, other: dict,
                 path: str, request_time: str, status: str):
        self.headers: Dict[str, str] = headers
        self.queries: Dict[str, List[str]] = queries
        self.one: ResponseSummary = ResponseSummary.from_dict(one)
        self.other: ResponseSummary = ResponseSummary.from_dict(other)
        self.path: str = path
        self.request_time: str = request_time
        self.status: Status = Status(status)


class ResponseSummary(OwlMixin):
    def __init__(self, status_code: int, byte: int, response_sec: int, url: str, file: Optional[str]=None):
        self.status_code: int = status_code
        self.byte: int = byte
        self.response_sec: int = response_sec
        self.url: str = url
        self.file: Optional[str] = file
