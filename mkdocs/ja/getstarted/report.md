Report
======

実行結果として出力されるレポート(`report.json`)について説明します。


## Definitions

### Report

| Key         | Type                | Description                             | Example                          |
|-------------|---------------------|-----------------------------------------|----------------------------------|
| version     | string              | 実行したJumeauxのバージョン             | 0.58.0                           |
| key         | string              | 実行ごとにユニークになるキー            | a1e4d ... 416422                 |
| title       | string              | タイトル                                | リグレッションテスト             |
| description | (string)            | 説明                                    | デグレを発見するためのテストです |
| summary     | [Summary](#summary) | 結果の概要                              |                                  |
| trials      | [Trial][trial][]    | テストリクエスト1つ1つの結果詳細        |                                  |
| addons      | [Addons][addons]    | 利用したアドオンの設定                  |                                  |
| retry_hash  | (string)            | リトライ対象のkey. リトライした場合のみ | a1e4d ... 416422                 |
| ignores     | Ignores[]           | ※ もうすぐ削除予定のため省略します      |                                  |


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
| threads   | int  | 実行スレッド数 :fa-exclamation-triangle: | 2       |
| processes | int  | 実行プロセス数                           | 2       |

!!! warning "threads"

    実際に使用したスレッド数は2倍になります。 (`one`と`other`へは2スレッドで同時にリクエストするため)


## Examples

TODO


[addons]: ../../addons#configration-definitions
[access-point]: ../../models/access-point
[trial]: ../../models/trial

