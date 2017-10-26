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
