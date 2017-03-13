# -*- coding:utf-8 -*-

import os
from decimal import Decimal
from owlmixin import OwlMixin
from modules.models import Report, OutputSummary
import boto3


class Config(OwlMixin):
    def __init__(self, table, bucket):
        self.table: str = table
        self.bucket: str = bucket


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
        "same_count": Decimal(report.summary.status.same),
        "different_count": Decimal(report.summary.status.different),
        "failure_count": Decimal(report.summary.status.failure),
        "start": report.summary.time.start,
        "end": report.summary.time.end
    }
    table.put_item(Item=item)

    # s3
    s3 = boto3.client('s3')

    def upload_responses(which: str):
        dir = f'{output_summary.response_dir}/{report.key}'
        for file in os.listdir(f'{dir}/{which}'):
            s3.upload_file(Bucket=config.bucket,
                           Key=f'{report.key}/{which}/{file}',
                           Filename=f'{dir}/{which}/{file}')

    # report
    s3.put_object(Bucket=config.bucket,
                  Key=f'{report.key}/report.json',
                  Body=report.to_json())

    # details
    upload_responses("one")
    upload_responses("other")

    return report
