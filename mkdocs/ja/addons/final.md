final [:fa-github:][s1]
=======================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final

Jumeauxの処理が完了する直前処理を行う事ができます。


[:fa-github:][summary] summary
------------------------------

[summary]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/summary.py

結果の概要をテキスト形式で出力します。  
出力された項目の定義は[report]を参考にしてください。


### Config

#### Definitions

##### Root

| Key    | Type   | Description                                       | Example | Default |
|--------|--------|---------------------------------------------------|---------|---------|
| sysout | (bool) | ファイルではなく標準出力を使うか :fa-info-circle: | true    | false   |

!!! info "sysout"

    * trueでない場合はファイルが作成されます
    * ファイルはconfigの[response_dir]で指定されたディレクトリの中に`summary.txt`という名前で作成されます


#### Examples

##### 結果の概要ファイルを出力する

```yaml
final:
  - name: summary
```

##### 結果の概要を標準出力に出力する

```yaml
final:
  - name: summary
    config:
      sysout: true
```


[:fa-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/json.py

結果のレポートをjson形式で出力します。  
出力されたjsonの定義は[report]を参照してください。


### Config

#### Definitions

##### Root

| Key    | Type   | Description                                       | Example | Default |
|--------|--------|---------------------------------------------------|---------|---------|
| sysout | (bool) | ファイルではなく標準出力を使うか :fa-info-circle: | true    | false   |
| indent | (int)  | インデント :fa-info-circle:                       | 2       | -       |

!!! info "sysout"

    * trueでない場合はファイルが作成されます
    * ファイルはconfigの[response_dir]で指定されたディレクトリの中に`report.json`という名前で作成されます

!!! info "indent"

    未指定だと1行で出力されます。

#### Examples

##### 結果のレポートをjsonファイルで出力する

```yaml
final:
  - name: json
```

##### 結果のレポートをインデントサイズ4で標準出力に出力する

```yaml
final:
  - name: json
    config:
      sysout: true
      indent: 4
```


[:fa-github:][miroir] miroir
----------------------------

[miroir]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/miroir.py

Miroir参照用にデータをAWSに登録します。


### Config

#### Definitions

##### Root

|       Key        |           Type            |                     Description                     |     Example      | Default |
| ---------------- | ------------------------- | --------------------------------------------------- | ---------------- | ------- |
| table            | string                    | 転送先DynamoDBのテーブル名                          | miroir           |         |
| bucket           | string                    | 転送先S3のBucket名                                  | mamansoft-miroir |         |
| prefix           | (string)                  | 転送先S3のkey prefix                                | test             |         |
| cache_max_age    | (int)                     | S3に転送したレスポンスのキャッシュ生存期間(秒)      | 3600             | 0       |
| with_zip         | (bool)                    | ReportとレスポンスをzipしたファイルをS3に転送するか | false            | true    |
| assumed_role_arn | (string)                  | Assumed roleで認証を行う場合はarnを指定する         | TODO:            |         |
| checklist        | (string)                  | 今はまだ使用していません                            |                  |         |
| local_stack      | [LocalStack](#localstack) | LocalStackを使用する場合に設定する                  |                  |         |
| when             | (When[])  | Miroirへ転送する条件                                |                  |         |

??? info "when"

    |   Name        |               Description               |
    | ------------- | --------------------------------------- |
    | not_empty     | 結果が空ではないとき                    |
    | has_different | 結果にdifferentが存在するとき           |

    * 全ての条件を満たす場合のみ転送します
    * 未指定の場合は必ず転送します

##### LocalStack

|   Key    |   Type   |        Description         |      Example      |     Default      |
| -------- | -------- | -------------------------- | ----------------- | ---------------- |
| use      | bool     | LocalStackを使用するか     | true              |                  |
| endpoint | (string) | LocalStackのエンドポイント | http://localstack | http://localhost |

#### Examples

##### キャッシュ1時間で保存する

```yaml
final:
  - name: miroir
    config:
      table: miroir
      bucket: mamansoft-miroir
      cache_max_age: 3600
```

##### キャッシュなしでprefixを指定して保存する

Bucketの`test/`配下にデータが保存されます。

```yaml
final:
  - name: miroir
    config:
      table: miroir
      bucket: mamansoft-miroir
      prefix: test
```

##### LocalStackを使ってキャッシュ2分で保存する

```yaml
final:
  - name: miroir
    config:
      table: miroir
      bucket: mamansoft-miroir
      cache_max_age: 120
      local_stack:
        use: true
```

##### 結果が空でないときだけ保存する

```yaml
final:
  - name: miroir
    config:
      table: miroir
      bucket: mamansoft-miroir
      when:
        - not_empty
```


[:fa-github:][slack] slack
--------------------------

[slack]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/slack.py

実行結果をSlackに転送します。

### Prerequirements

--8<-- "ja/notify-prerequirements.md"


### Config

#### Definitions

##### Root

|    Key     |           Type            |    Description     | Example | Default |
| ---------- | ------------------------- | ------------------ | ------- | ------- |
| conditions | [Condition](#condition)[] | 送信条件と送信内容 |         |         |

##### Condition

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

    [Report](../getstarted/report.md)で定義されたプロパティを使用する事ができます。

#### Examples

##### `#jumeaux` channelに終了時通知する

```yaml
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

```yaml
final:
  - name: slack
    config:
      conditions:
        - payload:
            message_format: "Version {version}, Title: {title}, -- {summary[status][different]} diffs"
            channel: "#jumeaux"
```

通知本文は `Version 0.24.1, Title: DEMO, -- 2 diffs` のようになります。


[:fa-github:][csv] csv
----------------------

[csv]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/csv.py

レポートの`trials`をCSVファイル形式で追加出力します。


### Config

#### Definitions

|     Key      |   Type   |               Description                |        Example        | Default |
| ------------ | -------- | ---------------------------------------- | --------------------- | ------- |
| column_names | string[] | 出力する要素名のリスト  :fa-info-circle: | `[seq, name, status]` |         |
| output_path  | string   | 出力するCSVファイルのパス                | result.csv            |         |
| with_header  | (bool)   | ヘッダ行を出力するか                     | true                  | false   |

??? info "column_names"

    以下の要素が有効です。

    |        Name        |            Description            |
    | ------------------ | --------------------------------- |
    | seq                | シーケンス                        |
    | name               | 名称                              |
    | path               | パス                              |
    | headers            | ヘッダ(JSON文字列)                |
    | queries            | クエリ(JSON文字列)                |
    | request_time       | リクエスト日時                    |
    | status             | ステータス                        |
    | one.url            | oneのリクエストURL                |
    | one.status         | oneのステータスコード             |
    | one.byte           | oneのレスポンスサイズ             |
    | one.response_sec   | oneのレスポンスタイム(秒)         |
    | one.content_type   | oneのコンテントタイプ             |
    | one.encoding       | oneのレスポンスエンコーディング   |
    | other.url          | otherのリクエストURL              |
    | other.status       | otherのステータスコード           |
    | other.byte         | otherのレスポンスサイズ           |
    | other.response_sec | otherのレスポンスタイム(秒)       |
    | other.content_type | otherのコンテントタイプ           |
    | other.encoding     | otherのレスポンスエンコーディング |


#### Examples

##### `seq` `name` `status` の要素を出力する

```yaml
final:
  - name: csv
    config:
      column_names:
        - seq
        - name
        - status
      output_path: result.csv
```

##### `seq` `name` `status`, `one.response_sec`, `other.response_sec` の要素をヘッダ付きで出力する

```yaml
final:
  - name: csv
    config:
      with_header: true
      column_names:
        - seq
        - name
        - status
        - one.response_sec
        - other.response_sec
      output_path: result.csv
```


[:fa-github:][viewer] viewer
----------------------------

[viewer]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/viewer.py

結果をGUIで確認するためのHTMLを出力します。

出力される`index.html`は同じディレクトリに以下のエントリがいる前提で動作します。

* oneディレクトリ
* otherディレクトリ
* report.json

`report.json`を作成するには`final/json`アドオンを指定してください。

### Config

#### Definitions

Config設定はありません。

#### Examples

##### 結果をGUIで確認するためのviewerを同梱する

```yaml
final:
  - name: json  # report.jsonが必要なため
  - name: viewer
```


[report]: https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/report
[response_dir]: https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/configuration/#outputsummary
