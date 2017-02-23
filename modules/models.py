# -*- coding: utf-8 -*-

from typing import Optional, Any
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict
from modules.requestcreator import *
from enum import Enum


class Format(Enum):
    PLAIN = "plain"
    APACHE = "apache"
    YAML = "yaml"
    CSV = "csv"


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
