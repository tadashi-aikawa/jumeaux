AccessPoint
===========

アクセス先情報の定義です。

Definitions
-----------

### AccessPoint

|            Key            |                    Type                     |                          Description                          |             Example             | Default |
| ------------------------- | ------------------------------------------- | ------------------------------------------------------------- | ------------------------------- | ------- |
| name                      | string                                      | アクセス先の名称                                              | Production                      |         |
| host                      | string                                      | アクセス先のhost                                              | `http://jumeaux/production`     |         |
| path                      | ([PathReplace](#pathreplace))               | アクセス先ごとにパスを置換したい場合の設定                    | -                               |         |
| query                     | ([QueryCustomization](#querycustomization)) | アクセス先ごとにクエリを上書き/削除したい場合の設定           | -                               |         |
| headers                   | (dict[string])                              | アクセス先ごとに追加するリクエストヘッダ                      | <pre>{"xxx": "xxx-value"}</pre> |         |
| proxy                     | (string)                                    | プロキシ :fa-exclamation-triangle:                            | `proxy-host`                    |         |
| default_response_encoding | (string)                                    | レスポンスのエンコーディングが不明な場合の値 :fa-info-circle: | utf8                            |         |

!!! warning "headers"

    [Request]に同名headerが指定されている場合はそちらが優先されます。

!!! warning  "proxy"

    スキーム(`http://`など)は設定しないでください。  
    内部でhttpとhttpsを割り当てます。

!!! info "default_response_encoding"

    未指定の場合はレスポンスボディの中身を解析してencodingを推測します。  
    推測はボディが大きい場合にパフォーマンスが著しく劣化するので可能な限り指定して下さい。

    content-typeにcharsetが指定されていれば本パラメータは無関係です。

### PathReplace

| Key    | Type     | Description                 | Example         | Default |
|--------|----------|-----------------------------|-----------------|---------|
| before | (string) | 置換対象の正規表現          | `([0-9]+).json` |         |
| after  | (string) | 置換後の値 :fa-info-circle: | `\\1.xml`       |         |


!!! info "after"

    `\\1`のように出現箇所を使用することもできます。


### QueryCustomization

| Key       | Type                 | Description                                       | Example                                   | Default |
|-----------|----------------------|---------------------------------------------------|-------------------------------------------|---------|
| overwrite | (dict[list[string]]) | 上書きクエリのkey-value :fa-exclamation-triangle: | <pre>{"a": ["v1"], "b": ["2", "3"]}</pre> |         |
| remove    | (list[string])       | 削除するクエリのリスト                            | `[id, name]`                              |         |

名前が`/i`で終わるキーはcase insensitive(大文字小文字を区別しない)になります。

!!! warning "overwrite"

    `overwrite`は既存のクエリに値を追加できません。  
    既にクエリの値が設定されている場合、それらは削除されます。

??? info "overwriteで使える$DATETIMEマクロについて"

    値に`$DATETIME`マクロを使うと現在時刻からの相対時刻に任意のフォーマットで置換できます。

    - フォーマットは`$DATETIME(フォーマット)(相対秒)`
    - 現在時刻が2021年4月18日20時52分00秒のとき
        - `$DATETIME(%Y-%m-%dT%H:%M:%S)(3600)`で`2021-04-18T21:52:00`になる
        - `$DATETIME(%Y/%m/%d)(-86400)`で`2021/04/17`になる

Examples
--------

### Production環境のアクセス先情報

```yml
name: Production
host: "http://jumeaux/production"
```

### パス中のoneをtwoに置換する

```yml
name: Path replace normal
host: "http://jumeaux/production"
path:
  before: one
  after: two
```

### パス中の先頭に出現する連続した数字を末尾に移動する

```yml
name: Path replace moving
host: "http://jumeaux/production"
path:
  before: "^(\\d+)(.+)"
  after: "\\2\\1"
```

### クエリ、idを123に上書きしnameを削除する (キーの大文字小文字を区別する)

```yml
name: Query Customization case sensitive
host: "http://jumeaux/production"
query:
  overwrite:
    id: ['123']
  remove:
    - name
```

### クエリ、idを123に上書きしnameを削除する (キーの大文字小文字を区別しない)

```yml
name: Query Customization case insensitive
host: "http://jumeaux/production"
query:
  overwrite:
    id/i: ['123']
  remove:
    - name/i
```

### 各テスト(trial)実行時の日時をクエリのtimeに追加/置換する

```yml
name: Add or replace time
host: "http://jumeaux/production"
query:
  overwrite:
    time: ['$DATETIME(%Y-%m-%dT%H:%M:%S)(0)']
```

### `proxy-host`をプロキシとして経由するProduction環境のアクセス先情報

```yml
name: Production
host: "http://jumeaux/production"
proxy: proxy-host
```

### レスポンスが不明な場合にeuc_jpと解釈させるProduction環境のアクセス先情報

```yml
name: Production
host: "http://jumeaux/production"
default_response_encoding: euc_jp
```

### User-AgentをSuper-Jumeauxで上書きする

```yml
name: Production
host: "http://jumeaux/production"
headers:
  User-Agent: Super-Jumeaux
```

[request]: ../../models/request
