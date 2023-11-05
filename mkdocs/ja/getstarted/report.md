Report
======

実行結果として出力されるレポート(`report.json`)について説明します。


## Definitions

### Report

| Key           | Type                         | Description                               | Example                          |     |
| ------------- | ---------------------------- | ----------------------------------------- | -------------------------------- | --- |
| version       | string                       | 実行したJumeauxのバージョン               | 0.58.0                           |     |
| key           | string                       | 実行ごとにユニークになるキー              | a1e4d ... 416422                 |     |
| title         | string                       | タイトル                                  | リグレッションテスト             |     |
| description   | (string)                     | 説明                                      | デグレを発見するためのテストです |     |
| notifiers     | (dict[[Notifier][notifier]]) | 通知設定                                  |                                  |     |
| summary       | [Summary](#summary)          | 結果の概要                                |                                  |     |
| trials        | [Trial][trial][]             | テストリクエスト1つ1つの結果詳細          |                                  |     |
| addons        | [Addons][addons]             | 利用したアドオンの設定                    |                                  |     |
| retry_hash    | (string)                     | リトライ対象のkey. リトライした場合のみ   | a1e4d ... 416422                 |     |
| ignores       | Ignores[]                    | ※ もうすぐ削除予定のため省略します       |                                  |     |


### Summary

| Key              | Type                            | Description            | Example                        |
|------------------|---------------------------------|------------------------|--------------------------------|
| one              | [AccessPoint][access-point]     | 比較元のアクセス先情報 |                                |
| other            | [AccessPoint][access-point]     | 比較先のアクセス先情報 |                                |
| tags             | (string[])                      | タグ                   | <pre>- test<br>- jumeaux</pre> |
| output           | [OutputSummary](#outputsummary) | 出力に関する設定       |                                |
| status           | [StatusCounts](#statuscounts)   | 各ステータスの数       |                                |
| time             | [Time](#time)                   | 時間情報               |                                |
| concurrency      | [Concurrency](#concurrency)     | 同時実行情報           |                                |
| default_encoding | (string)                        | ??? TODO               |                                |


### OutputSummary

|     Key      |       Type       |              Description               |    Example     |
| ------------ | ---------------- | -------------------------------------- | -------------- |
| response_dir | string           | レスポンスを格納するディレクトリのパス | test/responses |
| encoding     | (string)         | 出力するレポートのエンコーディング     | euc-jp         |

### StatusCounts

| Key       | Type | Description             | Example |
|-----------|------|-------------------------|---------|
| same      | int  | Sameと判定された数      | 2       |
| different | int  | Differentと判定された数 | 2       |
| failure   | int  | 試行に失敗した数        | 2       |

### Time

| Key         | Type   | Description  | Example                          |
|-------------|--------|--------------|----------------------------------|
| start       | string | 実行開始時間 | 2018-12-03T00:12:02.423035+09:00 |
| end         | string | 実行終了時間 | 2018-12-03T00:13:12.423035+09:00 |
| elapsed_sec | int    | 実行時間(秒) | 50                               |

### Concurrency

| Key       | Type | Description                              | Example |
|-----------|------|------------------------------------------|---------|
| threads   | int  | 実行スレッド数 :fontawesome-solid-triangle-exclamation: | 2       |
| processes | int  | 実行プロセス数                           | 2       |

!!! warning "threads"

    実際に使用したスレッド数は2倍になります。 (`one`と`other`へは2スレッドで同時にリクエストするため)


## Examples

`jumeaux init ignore`で作成したテンプレートを実行した結果です。

??? info "クリックしてreport.jsonの内容を見る"

    ```json
    {
      "addons": {
        "did_challenge": [],
        "dump": [
          {
            "cls_name": "Executor",
            "name": "json"
          }
        ],
        "final": [
          {
            "cls_name": "Executor",
            "name": "json"
          },
          {
            "cls_name": "Executor",
            "name": "viewer"
          }
        ],
        "judgement": [
          {
            "cls_name": "Executor",
            "config": {
              "ignores": [
                {
                  "conditions": [
                    {
                      "changed": [
                        {
                          "path": "root<'ignored_id'>"
                        }
                      ]
                    }
                  ],
                  "title": "Ignore ignored_id"
                },
                {
                  "conditions": [
                    {
                      "changed": [
                        {
                          "path": "root<'members'><\\d+><'name'>",
                          "when": "other == \"ignored\""
                        }
                      ]
                    }
                  ],
                  "title": "Ignore `members.name` which change to `ignored`"
                },
                {
                  "conditions": [
                    {
                      "added": [
                        {
                          "path": "root<'members'><\\d+><'favorite'>.*"
                        }
                      ],
                      "changed": [
                        {
                          "path": "root<'members'><\\d+><'favorite'>.*"
                        }
                      ],
                      "removed": [
                        {
                          "path": "root<'members'><\\d+><'favorite'>.*"
                        }
                      ],
                      "when": "\"same\" in req.path"
                    }
                  ],
                  "title": "Ignore favorite only if path includes `/same`"
                }
              ]
            },
            "name": "ignore"
          }
        ],
        "log2reqs": {
          "cls_name": "Executor",
          "name": "csv"
        },
        "reqs2reqs": [],
        "res2dict": [
          {
            "cls_name": "Executor",
            "name": "json"
          }
        ],
        "res2res": [],
        "store_criterion": [
          {
            "cls_name": "Executor",
            "config": {
              "when_any": [
                "status == 'different'"
              ]
            },
            "name": "free"
          }
        ]
      },
      "key": "398cdd3f0ddc2191dca8a5c7e9de9765d772585762ea5fc0b49ecaf7ed2ec78a",
      "summary": {
        "concurrency": {
          "processes": 1,
          "threads": 1
        },
        "one": {
          "headers": {},
          "host": "http://localhost:8000/api/one",
          "name": "One endpoint"
        },
        "other": {
          "headers": {},
          "host": "http://localhost:8000/api/other",
          "name": "Other endpoint"
        },
        "output": {
          "encoding": "utf8",
          "response_dir": "responses"
        },
        "status": {
          "different": 1,
          "failure": 0,
          "same": 2
        },
        "tags": [],
        "time": {
          "elapsed_sec": 0,
          "end": "2019-08-04T23:48:36.503226+09:00",
          "start": "2019-08-04T23:48:36.368831+09:00"
        }
      },
      "title": "Ignore",
      "trials": [
        {
          "diffs_by_cognition": {
            "Ignore favorite only if path includes `/same`": {
              "added": [
                "root<'members'><2><'favorite'>"
              ],
              "changed": [
                "root<'members'><1><'favorite'><0>"
              ],
              "removed": [
                "root<'members'><1><'favorite'><1>"
              ]
            },
            "Ignore ignored_id": {
              "added": [],
              "changed": [
                "root<'ignored_id'>"
              ],
              "removed": []
            }
          },
          "headers": {},
          "method": "GET",
          "name": "Regard as `Same` in spite of `Different` actually",
          "one": {
            "byte": 457,
            "content_type": "application/json",
            "encoding": "ascii",
            "mime_type": "application/json",
            "response_sec": 0.01,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/one/same-1.json?param1=hoge"
          },
          "other": {
            "byte": 497,
            "content_type": "application/json",
            "encoding": "ascii",
            "mime_type": "application/json",
            "response_sec": 0,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/other/same-1.json?param1=hoge"
          },
          "path": "/same-1.json",
          "queries": {
            "param1": [
              "hoge"
            ]
          },
          "request_time": "2019-08-04T23:48:36.370480+09:00",
          "seq": 1,
          "status": "same",
          "tags": []
        },
        {
          "diffs_by_cognition": {
            "Ignore `members.name` which change to `ignored`": {
              "added": [],
              "changed": [
                "root<'members'><2><'name'>"
              ],
              "removed": []
            }
          },
          "headers": {},
          "method": "GET",
          "name": "Regard as `Same` in spite of `Different` actually (with when)",
          "one": {
            "byte": 497,
            "content_type": "application/json",
            "encoding": "ascii",
            "mime_type": "application/json",
            "response_sec": 0.01,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/one/same-2.json?param1=hoge"
          },
          "other": {
            "byte": 499,
            "content_type": "application/json",
            "encoding": "ascii",
            "mime_type": "application/json",
            "response_sec": 0.01,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/other/same-2.json?param1=hoge"
          },
          "path": "/same-2.json",
          "queries": {
            "param1": [
              "hoge"
            ]
          },
          "request_time": "2019-08-04T23:48:36.418567+09:00",
          "seq": 2,
          "status": "same",
          "tags": []
        },
        {
          "diffs_by_cognition": {
            "Ignore ignored_id": {
              "added": [],
              "changed": [
                "root<'ignored_id'>"
              ],
              "removed": []
            },
            "unknown": {
              "added": [
                "root<'members'><2><'favorite'>"
              ],
              "changed": [
                "root<'members'><1><'favorite'><0>"
              ],
              "removed": [
                "root<'members'><1><'favorite'><1>"
              ]
            }
          },
          "headers": {},
          "method": "GET",
          "name": "Only ignore `ignored_id`",
          "one": {
            "byte": 457,
            "content_type": "application/json",
            "encoding": "ascii",
            "file": "one/(3)Only ignore `ignored_id`",
            "mime_type": "application/json",
            "prop_file": "one-props/(3)Only ignore `ignored_id`.json",
            "response_sec": 0.01,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/one/diff-1.json?param1=hoge&param1=hoge2&param2=huga"
          },
          "other": {
            "byte": 497,
            "content_type": "application/json",
            "encoding": "ascii",
            "file": "other/(3)Only ignore `ignored_id`",
            "mime_type": "application/json",
            "prop_file": "other-props/(3)Only ignore `ignored_id`.json",
            "response_sec": 0.01,
            "status_code": 200,
            "type": "json",
            "url": "http://localhost:8000/api/other/diff-1.json?param1=hoge&param1=hoge2&param2=huga"
          },
          "path": "/diff-1.json",
          "queries": {
            "param1": [
              "hoge",
              "hoge2"
            ],
            "param2": [
              "huga"
            ]
          },
          "request_time": "2019-08-04T23:48:36.456861+09:00",
          "seq": 3,
          "status": "different",
          "tags": []
        }
      ],
      "version": "2.0.0"
    }
    ```


[addons]: ../../addons#configration-definitions
[access-point]: ../../models/access-point
[trial]: ../../models/trial
[notifier]: ../../models/notifier
