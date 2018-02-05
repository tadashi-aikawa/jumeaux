# -*- coding:utf-8 -*-

from owlmixin import OwlEnum

import logging.config


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
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': level.value,
                'stream': 'ext://sys.stderr'
            }
        },
        'root': {
            'level': level.value,
            'handlers': ['console']
        }
    }


def init_logger(v_num: int):
    """
    Call when initialize Jumeaux !!
    :return:
    """
    logging.addLevelName(LogLevel.INFO_LV1.value, 'INFO_LV1')
    logging.addLevelName(LogLevel.INFO_LV2.value, 'INFO_LV2')
    logging.addLevelName(LogLevel.INFO_LV3.value, 'INFO_LV3')

    logging.config.dictConfig(create_logger_config({
        0: LogLevel.INFO_LV1,
        1: LogLevel.INFO_LV2,
        2: LogLevel.INFO_LV3,
        3: LogLevel.DEBUG,
    }[v_num]))


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
        self.logger.log(LogLevel.WARNING.value, msg)

    def error(self, msg):
        self.logger.log(LogLevel.ERROR.value, msg)

    def debug(self, msg):
        self.logger.log(LogLevel.DEBUG.value, msg)
