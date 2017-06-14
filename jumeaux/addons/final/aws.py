# -*- coding:utf-8 -*-

"""For example of config
final:
- name: jumeaux.addons.final.aws
  config:
    table:  jumeaux-report
    bucket: jumeaux-report
    cache_max_age: 600
"""

import logging
import shutil
from decimal import Decimal

import boto3
import os
import json
from owlmixin import OwlMixin

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import Report, OutputSummary, FinalAddOnPayload

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    def __init__(self, table, bucket, cache_max_age=0, with_zip=True, assumed_role_arn=None, checklist=None):
        self.table: str = table
        self.bucket: str = bucket
        self.cache_max_age: int = cache_max_age
        self.with_zip = with_zip
        self.assumed_role_arn = assumed_role_arn
        self.checklist = checklist


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        report: Report = payload.report
        output_summary: OutputSummary = payload.output_summary

        tmp_credential = boto3.client('sts').assume_role(
            RoleArn=self.config.assumed_role_arn,
            RoleSessionName='jumeaux_with_aws_add-on'
        ) if self.config.assumed_role_arn else None

        # dynamo
        dynamodb = boto3.resource('dynamodb', **({
            'aws_access_key_id': tmp_credential['Credentials']['AccessKeyId'],
            'aws_secret_access_key': tmp_credential['Credentials']['SecretAccessKey'],
            'aws_session_token': tmp_credential['Credentials']['SessionToken']
        } if tmp_credential else {}))

        table = dynamodb.Table(self.config.table)
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
            "end_time": report.summary.time.end,
            "with_zip": self.config.with_zip,
            "retry_hash": report.retry_hash,
            "check_status": 'todo'
        }
        if report.description:
            item['description'] = report.description
        if self.config.checklist:
            item['checklist'] = self.config.checklist
        table.put_item(Item=item)

        # s3
        s3 = boto3.client('s3', **({
            'aws_access_key_id': tmp_credential['Credentials']['AccessKeyId'],
            'aws_secret_access_key': tmp_credential['Credentials']['SecretAccessKey'],
            'aws_session_token': tmp_credential['Credentials']['SessionToken']
        } if tmp_credential else {}))

        def upload_responses(which: str):
            dir = f'{output_summary.response_dir}/{report.key}'
            for file in os.listdir(f'{dir}/{which}'):
                with open(f'{dir}/{which}/{file}', 'rb') as f:
                    logger.info(f'Put {dir}/{which}/{file}')
                    s3.put_object(Bucket=self.config.bucket,
                                  Key=f'jumeaux-results/{report.key}/{which}/{file}',
                                  Body=f.read(),
                                  CacheControl=f'max-age={self.config.cache_max_age}')

        # report
        # TODO: Immutable...
        d = report.to_dict()
        del d['trials']
        s3.put_object(Bucket=self.config.bucket,
                      Key=f'jumeaux-results/{report.key}/report-without-trials.json',
                      Body=json.dumps(d, ensure_ascii=False))
        s3.put_object(Bucket=self.config.bucket,
                      Key=f'jumeaux-results/{report.key}/trials.json',
                      Body=report.trials.to_json())

        # details
        upload_responses("one")
        upload_responses("other")

        # zip (${hashkey}.zip)
        if self.config.with_zip:
            base_name = f'{output_summary.response_dir}/{report.key}'
            with open(f'{base_name}/report.json', 'w', encoding=output_summary.encoding) as f:
                f.write(report.to_pretty_json())
            shutil.make_archive(base_name, 'zip', f'{output_summary.response_dir}/{report.key}')

            zip_fullpath = f'{base_name}.zip'
            with open(zip_fullpath, 'rb') as f:
                logger.info(f'Put {zip_fullpath}')
                s3.put_object(Bucket=self.config.bucket,
                              Key=f'jumeaux-results/{report.key}/{report.key[0:7]}.zip',
                              Body=f.read(),
                              CacheControl=f'max-age={self.config.cache_max_age}')
            os.remove(zip_fullpath)

        return payload
