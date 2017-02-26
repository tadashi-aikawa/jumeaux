# -*- coding:utf-8 -*-

import os
import json
from decimal import Decimal

import boto3


def main(report, config, output_summary):

    # dynamo
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=config['aws_access_key_id'],
                              aws_secret_access_key=config['aws_secret_access_key'],
                              region_name=config['region'])
    table = dynamodb.Table(config['table'])
    item = {
        "hashkey": report.key,
        "title": report.title,
        "one_host": report.summary.one.host,
        "other_host": report.summary.other.host,
        "same_count": Decimal(report.summary.status.same),
        "different_count": Decimal(report.summary.status.different),
        "start": report.summary.time.start,
        "end": report.summary.time.end,
        "report": json.loads(report.to_json(), parse_float=Decimal)
    }
    table.put_item(Item=item)

    # s3
    s3 = boto3.client('s3',
                      aws_access_key_id=config['aws_access_key_id'],
                      aws_secret_access_key=config['aws_secret_access_key'],
                      region_name=config['region'])

    dir = os.path.join(output_summary.response_dir, report.key)
    for file in os.listdir(dir):
        s3.upload_file(Bucket=config['bucket'],
                       Key=f'{report.key}/{file}',
                       Filename=f'{dir}/{file}')

    return report
