final [:fontawesome-brands-github:][s1]
=======================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final

Jumeauxの処理が完了する直前処理を行う事ができます。


[:fontawesome-brands-github:][summary] summary
------------------------------

[summary]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/summary.py

結果の概要をテキスト形式で出力します。  
出力された項目の定義は[report]を参考にしてください。


### Config

#### Definitions

##### Root

| Key    | Type   | Description                                       | Example | Default |
|--------|--------|---------------------------------------------------|---------|---------|
| sysout | (bool) | ファイルではなく標準出力を使うか :fontawesome-solid-circle-exclamation: | true    | false   |

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


[:fontawesome-brands-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/json.py

結果のレポートをjson形式で出力します。  
出力されたjsonの定義は[report]を参照してください。


### Config

#### Definitions

##### Root

| Key    | Type   | Description                                       | Example | Default |
|--------|--------|---------------------------------------------------|---------|---------|
| sysout | (bool) | ファイルではなく標準出力を使うか :fontawesome-solid-circle-exclamation: | true    | false   |
| indent | (int)  | インデント :fontawesome-solid-circle-exclamation:                       | 2       | -       |

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


[:fontawesome-brands-github:][miroir] miroir
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


[:fontawesome-brands-github:][notify] notify
----------------------------

[notify]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/notify.py

実行結果を通知します。


### Prerequirements

--8<-- "ja/notify-prerequirements.md"


### Config

#### Definitions

##### root

|   Key    |         Type          |        Description         | Example | Default |
| -------- | --------------------- | -------------------------- | ------- | ------- |
| notifies | ([Notify[]](#notify)) | 通知設定                    |         |         |

##### Notify

| Key      | Type   | Description                              | Example                                                 | Default |
| -------- | ------ | ---------------------------------------- | ------------------------------------------------------- | ------- |
| notifier | string | 使用する通知設定の名前  :fontawesome-solid-circle-exclamation: | jumeaux                                                 |         |
| message  | string | 送信するメッセージ :fontawesome-solid-circle-exclamation:      | <pre>{{ title }}が完了しました</pre>                    |         |
| when     | str    | 通知条件式 :fontawesome-solid-circle-exclamation:              | <pre>'summary.status.different > 0'</pre>               |         |


!!! info "notifierについて"

    通知設定の例は [config/examples] を参考にしてください。定義は [notifier] の通りです。

!!! info "messageについて"

    [Template表記]に対応しています。
    プロパティは[Report](../getstarted/report.md)で定義されたものを使用できます。

!!! info "whenで指定できるプロパティ"

    [Template表記]に対応しています。
    プロパティは[Report](../getstarted/report.md)で定義されたものを使用できます。

#### Examples

紹介する例は`jumeaux`という名前の[notifier]が設定されている必要があります。

??? note "設定例"
    ```yaml
    notifiers:
      jumeaux:
        type: slack
        version: 2
    ```

##### 通知設定`jumeaux`を使って終了時通知する

```yaml
  final:
    - name: notify
      config:
        notifies:
          - notifier: jumeaux
            message: "{{ title }} is Finish!! There are {{ summary.status.different }} diffs.."
```

##### differentのstatusが存在するときのみ通知する

```yaml
  final:
    - name: notify
      config:
        notifies:
          - notifier: jumeaux
            message: "There are {{ summary.status.different }} diffs.."
            when: "summary.status.different > 0"
```

[:fontawesome-brands-github:][csv] csv
----------------------

[csv]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/final/csv.py

レポートの`trials`をCSVファイル形式で追加出力します。


### Config

#### Definitions

|     Key      |   Type   |               Description                |        Example        | Default |
| ------------ | -------- | ---------------------------------------- | --------------------- | ------- |
| column_names | string[] | 出力する要素名のリスト  :fontawesome-solid-circle-exclamation: | `[seq, name, status]` |         |
| output_path  | string   | 出力するCSVファイルのパス                | result.csv            |         |
| with_header  | (bool)   | ヘッダ行を出力するか                     | true                  | false   |

??? info "column_names"

    以下の要素が有効です。

    |        Name        |            Description            |
    | ------------------ | --------------------------------- |
    | seq                | シーケンス                        |
    | name               | 名称                              |
    | method             | HTTPメソッド                      |
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


[:fontawesome-brands-github:][viewer] viewer
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


[Template表記]: ../../template
[report]: ../../getstarted/report
[response_dir]: ../../getstarted/configuration/#outputsummary
[notifier]: ../../models/notifier
[config/examples]: ../../getstarted/configuration/#examples

