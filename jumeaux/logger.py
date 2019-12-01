# -*- coding:utf-8 -*-

from owlmixin import OwlEnum

import sys
import logging.config


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    END = "\033[0m"
    BOLD = "\038[1m"
    UNDERLINE = "\033[4m"
    INVISIBLE = "\033[08m"
    REVERCE = "\033[07m"


class LogLevel(OwlEnum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO_LV1 = 20
    INFO_LV2 = 18
    INFO_LV3 = 16
    DEBUG = 10
    NOTSET = 0


def create_logger_config(level: LogLevel):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"simple": {"format": "%(message)s"}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": level.value,
                "stream": "ext://sys.stderr",
            }
        },
        "root": {"level": level.value, "handlers": ["console"]},
    }


def init_logger(v_num: int):
    """
    Call when initialize Jumeaux !!
    :return:
    """
    logging.addLevelName(
        LogLevel.INFO_LV1.value, "INFO_LV1"  # type: ignore # Prevent for enum problem
    )
    logging.addLevelName(
        LogLevel.INFO_LV2.value, "INFO_LV2"  # type: ignore # Prevent for enum problem
    )
    logging.addLevelName(
        LogLevel.INFO_LV3.value, "INFO_LV3"  # type: ignore # Prevent for enum problem
    )

    logging.config.dictConfig(
        create_logger_config(
            {  # type: ignore # Prevent for enum problem
                0: LogLevel.INFO_LV1,
                1: LogLevel.INFO_LV2,
                2: LogLevel.INFO_LV3,
                3: LogLevel.DEBUG,
            }[v_num]
        )
    )


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info_lv1(self, msg):
        self.logger.log(LogLevel.INFO_LV1.value, msg)

    def info_lv2(self, msg):
        self.logger.log(LogLevel.INFO_LV2.value, msg)

    def info_lv3(self, msg):
        self.logger.log(LogLevel.INFO_LV3.value, msg)

    def warning(self, msg):
        self.logger.log(LogLevel.WARNING.value, f"{Color.YELLOW}[WARNING] {msg}{Color.END}")

    def error(self, msg, exit=False):
        self.logger.log(LogLevel.ERROR.value, f"{Color.RED}[ ERROR ] {msg}{Color.END}")
        if exit:
            sys.exit(1)

    def debug(self, msg):
        self.logger.log(LogLevel.DEBUG.value, f"{Color.GREEN}[ DEBUG ] {msg}{Color.END}")
