# -*- coding:utf-8 -*-

"""For example of config
final:
- name: jumeaux.addons.final.aws
  config:
    table:  jumeaux-report
    bucket: jumeaux-report
    cache_max_age: 600
"""

import json
import logging
import os
import shutil
from decimal import Decimal

import boto3
from owlmixin import OwlMixin, TOption

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import Report, OutputSummary, FinalAddOnPayload

logger = logging.getLogger(__name__)


class LocalStack(OwlMixin):
    use: bool
    endpoint: str = 'http://localhost'


class Config(OwlMixin):
    table: str
    bucket: str
    cache_max_age: int = 0
    with_zip: bool = True
    assumed_role_arn: TOption[str]
    checklist: TOption[str]
    local_stack: TOption[LocalStack]


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: FinalAddOnPayload) -> FinalAddOnPayload:
        report: Report = payload.report
        output_summary: OutputSummary = payload.output_summary

        tmp_credential = boto3.client('sts').assume_role(
            RoleArn=self.config.assumed_role_arn.get(),
            RoleSessionName='jumeaux_with_aws_add-on'
        ) if not self.config.assumed_role_arn.is_none() else None

        def create_endpoint_url(port_as_localstack: int):
            return f'{self.config.local_stack.get().endpoint}:{port_as_localstack}'\
                if not self.config.local_stack.is_none() and self.config.local_stack.get().use else None

        # dynamo
        dynamodb = boto3.resource('dynamodb', **({
            'aws_access_key_id': tmp_credential['Credentials']['AccessKeyId'],
            'aws_secret_access_key': tmp_credential['Credentials']['SecretAccessKey'],
            'aws_session_token': tmp_credential['Credentials']['SessionToken'],
            'endpoint_url': create_endpoint_url(4569)
        } if tmp_credential else {'endpoint_url': create_endpoint_url(4569)}))

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
            "retry_hash": report.retry_hash.get(),
            "check_status": 'todo'
        }
        if not report.description.is_none():
            item['description'] = report.description.get()
        if not self.config.checklist.is_none():
            item['checklist'] = self.config.checklist.get()
        table.put_item(Item=item)

        # s3
        s3 = boto3.client('s3', **({
            'aws_access_key_id': tmp_credential['Credentials']['AccessKeyId'],
            'aws_secret_access_key': tmp_credential['Credentials']['SecretAccessKey'],
            'aws_session_token': tmp_credential['Credentials']['SessionToken'],
            'endpoint_url': create_endpoint_url(4572)
        } if tmp_credential else {'endpoint_url': create_endpoint_url(4572)}))

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
