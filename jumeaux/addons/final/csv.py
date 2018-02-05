# -*- coding:utf-8 -*-

import logging

from owlmixin import OwlMixin, TList

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import FinalAddOnPayload
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    column_names: TList[str]
    output_path: str
    with_header: bool = False


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        payload.report.trials.map(lambda x: {
            "seq": x.seq,
            "name": x.name,
            "path": x.path,
            "headers": x.headers.to_json(),
            "queries": x.queries.to_json(),
            "request_time": x.request_time,
            "status": x.status,
            "one.url": x.one.url,
            "one.status": x.one.status_code,
            "one.byte": x.one.byte,
            "one.response_sec": x.one.response_sec,
            "one.content_type": x.one.content_type,
            "one.encoding": x.one.encoding,
            "other.url": x.other.url,
            "other.status": x.other.status_code,
            "other.byte": x.other.byte,
            "other.response_sec": x.other.response_sec,
            "other.content_type": x.other.content_type,
            "other.encoding": x.other.encoding,
        }).to_csvf(
            fpath=self.config.output_path,
            fieldnames=self.config.column_names,
            with_header=self.config.with_header
        )

        return payload
