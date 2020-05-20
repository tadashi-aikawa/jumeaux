"""Retry Jumeaux from report
Usage:
  {cli} <report> [--title=<title>] [--description=<description>]
                 [--tag=<tag>...] [--threads=<threads>] [--processes=<processes>]
                 [--max-retries=<max_retries>] [-vvv]
  {cli} (-h | --help)

Options:
  <report>                                      Report for retry
  --title = <title>                             The title of report [def: No title]
  --description = <description>                 The description of report
  --tag = <tag>...                              Tags
  --threads = <threads>                         The number of threads in challenge [def: 1]
  --processes = <processes>                     The number of processes in challenge
  --max-retries = <max_retries>                 The max number of retries which accesses to API
  -vvv                                          Logger level (`-v` or `-vv` or `-vvv`)
  -h --help                                     Show this screen.
"""

from typing import Optional

from owlmixin import OwlMixin, TList
from owlmixin import TOption

from jumeaux import executor
from jumeaux.domain.config.vo import MergedArgs
from jumeaux.logger import Logger, init_logger

logger: Logger = Logger(__name__)


class Args(OwlMixin):
    report: str
    title: TOption[str]
    description: TOption[str]
    tag: TList[str]
    threads: TOption[int]
    processes: TOption[int]
    max_retries: TOption[int]
    v: int


def run(args: Args):
    init_logger(args.v)
    executor.retry(
        args=MergedArgs.from_dict(
            {
                "title": args.title,
                "description": args.description,
                "tag": TOption(args.tag or []),
                "threads": args.threads,
                "processes": args.processes,
                "max_retries": args.max_retries,
            }
        ),
        report=args.report,
    )
