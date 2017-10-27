final [:fa-github:][s1]
=======================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final

Jumeauxの処理が完了する直前処理を行う事ができます。


[:fa-github:][s2] aws
---------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/aws.py

AWSに結果を転送します。
転送した結果は[Jumeaux Viewer]などで参照するために利用します。

[Jumeaux Viewer]: https://github.com/tadashi-aikawa/jumeaux-viewer

### Config

#### Definitions

##### Root

|       Key        |           Type            |                     Description                     |         Example          | Default |
| ---------------- | ------------------------- | --------------------------------------------------- | ------------------------ | ------- |
| table            | string                    | 転送先DynamoDBのテーブル名                          | jumeaux-result           |         |
| bucket           | string                    | 転送先S3のBucket名                                  | mamansoft-jumeaux-result |         |
| cache_max_age    | (int)                     | S3に転送したレスポンスのキャッシュ生存期間(秒)      | 3600                     | 0       |
| with_zip         | (bool)                    | ReportとレスポンスをzipしたファイルをS3に転送するか | false                    | true    |
| assumed_role_arn | (string)                  | Assumed roleで認証を行う場合はarnを指定する         | TODO:                    |         |
| checklist        | (string)                  | 今はまだ使用していません                            |                          |         |
| local_stack      | [LocalStack](#localstack) | LocalStackを使用する場合に設定する                  |                          |         |

##### LocalStack

|   Key    |   Type   |        Description         |      Example      |     Default      |
| -------- | -------- | -------------------------- | ----------------- | ---------------- |
| use      | bool     | LocalStackを使用するか     | true              |                  |
| endpoint | (string) | LocalStackのエンドポイント | http://localstack | http://localhost |


#### Examples

##### LocalStackを使わない (キャッシュ1時間)

```yml
final:
  - name: aws
    config:
      table: jumeaux-viewer
      bucket: mamansoft-jumeaux-viewer
      cache_max_age: 3600
```

##### LocalStackを使う (キャッシュ2分)

```yml
final:
  - name: aws
    config:
      table: jumeaux-viewer
      bucket: mamansoft-jumeaux-viewer
      cache_max_age: 120
      local_stack:
        use: true
```



[:fa-github:][s3] slack
-----------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/slack.py

実行結果をSlackに転送します。

### Prerequirements

環境変数 `SLACK_INCOMING_WEBHOOKS_URL` に[Incoming webhook]のURIを設定して下さい

[Incoming webhook]: https://api.slack.com/incoming-webhooks


### Config

#### Definitions

#### Root

|    Key     |           Type            |    Description     | Example | Default |
| ---------- | ------------------------- | ------------------ | ------- | ------- |
| conditions | [Condition](#condition)[] | 送信条件と送信内容 |         |         |

#### Condition

|   Key   |        Type         |      Description      | Example | Default |
| ------- | ------------------- | --------------------- | ------- | ------- |
| payload | [Payload](#payload) | Slack送信に関する情報 |         |         |

##### Payload

|      Key       |   Type   |              Description              |        Example        | Default |
| -------------- | -------- | ------------------------------------- | --------------------- | ------- |
| message_format | string   | フォーマット付き本文 :fa-info-circle: |                       |         |
| channel        | string   | 送信先channel                         | #hoge                 |         |
| username       | string   | 投稿ユーザ名                          | Jumeaux man           | jumeaux |
| icon_emoji     | (string) | アイコン(絵文字表記)                  | `:smile:`             |         |
| icon_url       | (string) | アイコン(URL)                         | http://hoge/image.jpg |         |

!!! info "フォーマットについて"

    [Report](/getstarted/report.md)で定義されたプロパティを使用する事ができます。

#### Examples

##### `#jumeaux` channelに終了時通知する

```yml
final:
  - name: slack
    config:
      conditions:
        - payload:
            message_format: Finish Jumeaux!!
            channel: "#jumeaux"
            icon_emoji: ":innocent:"
```

##### メッセージフォーマットを利用して通知する

```yml
  final:
    - name: slack
      config:
        conditions:
          - payload:
              message_format: "Version {version}, Title: {title}, -- {summary[status][different]} diffs"
              channel: "#jumeaux"
```

通知本文は `Version 0.24.1, Title: DEMO, -- 2 diffs` のようになります。
