# -*- coding:utf-8 -*-

import os
import logging
from decimal import Decimal

from owlmixin import OwlMixin
from modules.models import Report, OutputSummary
import boto3

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, table, bucket, cache_max_age=0):
        self.table: str = table
        self.bucket: str = bucket
        self.cache_max_age: int = cache_max_age


def exec(report: Report, config_dict: dict, output_summary: OutputSummary):
    config: Config = Config.from_dict(config_dict or {})

    # dynamo
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(config.table)
    item = {
        "hashkey": report.key,
        "title": report.title,
        "one_host": report.summary.one.host,
        "other_host": report.summary.other.host,
        "paths": set(report.summary.paths),
        "same_count": Decimal(report.summary.status.same),
        "different_count": Decimal(report.summary.status.different),
        "failure_count": Decimal(report.summary.status.failure),
        "begin_time": report.summary.time.start,
        "end_time": report.summary.time.end
    }
    table.put_item(Item=item)

    # s3
    s3 = boto3.client('s3')

    def upload_responses(which: str):
        dir = f'{output_summary.response_dir}/{report.key}'
        for file in os.listdir(f'{dir}/{which}'):
            with open(f'{dir}/{which}/{file}', 'rb') as f:
                logger.info(f'Put {dir}/{which}/{file}')
                s3.put_object(Bucket=config.bucket,
                              Key=f'{report.key}/{which}/{file}',
                              Body=f.read(),
                              CacheControl=f'max-age={config.cache_max_age}')

    # report
    s3.put_object(Bucket=config.bucket,
                  Key=f'{report.key}/report.json',
                  Body=report.to_json())

    # details
    upload_responses("one")
    upload_responses("other")

    return report
