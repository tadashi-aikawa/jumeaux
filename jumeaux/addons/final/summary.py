# -*- coding:utf-8 -*-

import os
from owlmixin import OwlMixin

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import FinalAddOnPayload, Report, OutputSummary
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)


class Config(OwlMixin):
    sysout: bool = False


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        r: Report = payload.report
        s: OutputSummary = payload.output_summary

        summary: str = f"""
===================================================================
| {r.title}
===================================================================
{os.linesep + r.description.get() + os.linesep if r.description.get() else ''}
-------------------------------------------------------------------
| key   | {r.key}
| One   | {r.summary.one.host} ({r.summary.one.name})
| Other | {r.summary.other.host} ({r.summary.other.name})
-------------------------------------------------------------------

-------------------------------------------------------------------
|        Same         |      Differenct     |       Failure       |
-------------------------------------------------------------------
|{r.summary.status.same:^21}|{r.summary.status.different:^21}|{r.summary.status.failure:^21}|
-------------------------------------------------------------------

-------------------------------------------------------------------
| Threads         | {r.summary.concurrency.threads}
| Processes       | {r.summary.concurrency.processes}
| Begin           | {r.summary.time.start}
| End             | {r.summary.time.end}
| Elapsed seconds | {r.summary.time.elapsed_sec}
-------------------------------------------------------------------


>>> By Jumeaux {r.version}
"""

        if self.config.sysout:
            print(summary)
        else:
            with open(f"{payload.result_path}/summary.txt", "w", encoding=s.encoding) as f:
                f.write(summary)

        return payload
