#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest

from jumeaux.addons.final.miroir import Executor
from jumeaux.models import FinalAddOnPayload


def create_payload(tmpdir):
    response_dir = tmpdir.mkdir("responses")
    result_dir = response_dir.mkdir("report-key")

    for which in ["one", "one-props", "other", "other-props"]:
        response_subdir = result_dir.mkdir(which)
        response_subdir.join("1.json").write('{"ok": true}')

    return FinalAddOnPayload.from_dict(
        {
            "report": {
                "version": "6.0.1",
                "key": "report-key",
                "title": "title",
                "description": None,
                "notifiers": None,
                "summary": {
                    "one": {"name": "one", "host": "http://one", "headers": {}},
                    "other": {"name": "other", "host": "http://other", "headers": {}},
                    "status": {"same": 1, "different": 1, "failure": 0},
                    "tags": [],
                    "time": {
                        "start": "2026/03/11 00:00:00",
                        "end": "2026/03/11 00:00:01",
                        "elapsed_sec": 1,
                    },
                    "concurrency": {"threads": 1, "processes": 1},
                    "output": {"response_dir": str(response_dir), "encoding": "utf8"},
                    "default_encoding": None,
                },
                "trials": [],
                "addons": None,
                "retry_hash": None,
            },
            "output_summary": {"response_dir": str(response_dir), "encoding": "utf8"},
        }
    )


class FakeTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):
        self.items.append(Item)


class FakeDynamoResource:
    def __init__(self):
        self.table = FakeTable()
        self.table_name = None

    def Table(self, name):
        self.table_name = name
        return self.table


class FakeS3Client:
    def __init__(self):
        self.objects = []

    def put_object(self, **kwargs):
        self.objects.append(kwargs)


class Recorder:
    def __init__(self):
        self.resource_calls = []
        self.client_calls = []
        self.dynamo_resource = FakeDynamoResource()
        self.s3_client = FakeS3Client()

    def resource(self, service_name, **kwargs):
        self.resource_calls.append({"service_name": service_name, **kwargs})
        return self.dynamo_resource

    def client(self, service_name, **kwargs):
        self.client_calls.append({"service_name": service_name, **kwargs})
        return self.s3_client


class TestExec:
    def test_uses_endpoints_when_configured(self, monkeypatch, tmpdir):
        recorder = Recorder()
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.resource", recorder.resource)
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.client", recorder.client)

        payload = create_payload(tmpdir)

        Executor(
            {
                "table": "miroir",
                "bucket": "mamansoft-miroir",
                "endpoints": {
                    "dynamodb": "http://localhost:3456",
                    "s3": "http://localhost:3457",
                },
                "with_zip": False,
            }
        ).exec(payload, None)

        assert recorder.resource_calls == [
            {"service_name": "dynamodb", "endpoint_url": "http://localhost:3456"}
        ]
        assert recorder.client_calls == [
            {"service_name": "s3", "endpoint_url": "http://localhost:3457"}
        ]

    def test_uses_local_stack_ports_when_enabled(self, monkeypatch, tmpdir):
        recorder = Recorder()
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.resource", recorder.resource)
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.client", recorder.client)

        payload = create_payload(tmpdir)

        Executor(
            {
                "table": "miroir",
                "bucket": "mamansoft-miroir",
                "local_stack": {"use": True, "endpoint": "http://localhost"},
                "with_zip": False,
            }
        ).exec(payload, None)

        assert recorder.resource_calls == [
            {"service_name": "dynamodb", "endpoint_url": "http://localhost:4569"}
        ]
        assert recorder.client_calls == [
            {"service_name": "s3", "endpoint_url": "http://localhost:4572"}
        ]

    def test_uses_none_when_no_endpoint_settings(self, monkeypatch, tmpdir):
        recorder = Recorder()
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.resource", recorder.resource)
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.client", recorder.client)

        payload = create_payload(tmpdir)

        Executor(
            {
                "table": "miroir",
                "bucket": "mamansoft-miroir",
                "with_zip": False,
            }
        ).exec(payload, None)

        assert recorder.resource_calls == [{"service_name": "dynamodb", "endpoint_url": None}]
        assert recorder.client_calls == [{"service_name": "s3", "endpoint_url": None}]

    def test_allows_partial_endpoints(self, monkeypatch, tmpdir):
        recorder = Recorder()
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.resource", recorder.resource)
        monkeypatch.setattr("jumeaux.addons.final.miroir.boto3.client", recorder.client)

        payload = create_payload(tmpdir)

        Executor(
            {
                "table": "miroir",
                "bucket": "mamansoft-miroir",
                "endpoints": {"dynamodb": "http://localhost:3456", "s3": None},
                "with_zip": False,
            }
        ).exec(payload, None)

        assert recorder.resource_calls == [
            {"service_name": "dynamodb", "endpoint_url": "http://localhost:3456"}
        ]
        assert recorder.client_calls == [{"service_name": "s3", "endpoint_url": None}]

    def test_rejects_endpoints_with_local_stack(self):
        with pytest.raises(
            ValueError,
            match="miroir config: endpoints and local_stack cannot be used together",
        ):
            Executor(
                {
                    "table": "miroir",
                    "bucket": "mamansoft-miroir",
                    "local_stack": {"use": True, "endpoint": "http://localhost"},
                    "endpoints": {
                        "dynamodb": "http://localhost:3456",
                        "s3": "http://localhost:3456",
                    },
                }
            )
