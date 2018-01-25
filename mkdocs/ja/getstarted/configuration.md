Configuration
=============

設定ファイル(デフォルト`config.yml`)について説明します。

## Definitions

### Config

|     Key     |              Type               |                Description                |            Example             | Default  |
| ----------- | ------------------------------- | ----------------------------------------- | ------------------------------ | -------- |
| one         | [AccessPoint][access-point]     | 比較元のアクセス先情報                    |                                |          |
| other       | [AccessPoint][access-point]     | 比較先のアクセス先情報                    |                                |          |
| output      | [OutputSummary](#outputsummary) | 出力に関する設定                          |                                |          |
| threads     | (int)                           | 実行スレッド数  :fa-exclamation-triangle: | 2                              | 1        |
| processes   | (int)                           | 実行プロセス数  :fa-exclamation-triangle: | 2                              | 1        |
| max_retries | (int)                           | 接続エラー時の最大リトライ数              | 0                              | 3        |
| title       | (string)                        | タイトル                                  | Test                           | No title |
| description | (string)                        | 説明                                      | Running for test               |          |
| tags        | (string[])                      | タグ                                      | <pre>- test<br>- jumeaux</pre> |          |
| notifiers   | (dict[[Notifier][notifier]])    | 通知設定  :fa-info-circle:                |                                |          |
| addons      | [Addons][addons]                | 利用するアドオンの設定                    |                                |          |

!!! warning "threads"

    実際に使用するスレッド数は指定した数の2倍になります。 (`one`と`other`へは2スレッドで同時にリクエストするため)

!!! warning "threadsとprocessesを指定した場合"

    `threads`と`processes`の両方を指定した場合、スレッド数は1になります。

!!! info "notifiers"

    アドオンなどで通知が必要な場合、notifiersのキーを指定します。

### OutputSummary

!!! danger

    `logger`の仕様は近いうちに破壊的変更があります。

|     Key      |       Type       |              Description               |    Example     | Default |
| ------------ | ---------------- | -------------------------------------- | -------------- | ------- |
| response_dir | string           | レスポンスを格納するディレクトリのパス | test/responses |         |
| encoding     | (string)         | 出力するレポートのエンコーディング     | euc-jp         | utf8    |
| logger       | :fa-info-circle: | ロガー設定                             |                |         |

!!! info "logger"

    [pythonのlogging設定](http://wingware.com/psupport/python-manual/3.4/library/logging.config.html#logging-config-dictschema)に準拠します。


## Examples

### リクエストが空だと通知するconfigの例

```yml
title: Test
Description: Running for test

one:
  name: One
  host: https://raw.githubusercontent.com/tadashi-aikawa/jumeaux-toolbox/master/vagrant/ignore_properties/one

other:
  name: Other
  host: https://raw.githubusercontent.com/tadashi-aikawa/jumeaux-toolbox/master/vagrant/ignore_properties/other

notifiers:
  test:
    type: slack
    channel: "#times_tadashi-aikawa"
    icon_emoji: "innocent"

output:
  response_dir: responses
  logger:  # (See http://wingware.com/psupport/python-manual/3.4/library/logging.config.html#logging-config-dictschema)
    version: 1
    formatters:
      simple:
        format: '%(levelname)s %(message)s'
    handlers:
      console:
        class : logging.StreamHandler
        formatter: simple
        level   : INFO
        stream  : ext://sys.stderr
    root:
      level: INFO
      handlers: [console]

addons:
  log2reqs:
    name: plain

  reqs2reqs:
    - name: empty_guard
      config:
        notifies:
          - notifier: test
            message: "{title} notify!"
```

[addons]: /ja/addons/index
[notifier]: /ja/models/notifier
[access-point]: /ja/models/access-point
