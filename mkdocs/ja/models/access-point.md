AccessPoint
===========

アクセス先情報の定義です。

Definitions
-----------

### AccessPoint

| Key                       | Type                                        | Description                                                   | Example                     | Default |
|---------------------------|---------------------------------------------|---------------------------------------------------------------|-----------------------------|---------|
| name                      | string                                      | アクセス先の名称                                              | Production                  |         |
| host                      | string                                      | アクセス先のhost                                              | `http://jumeaux/production` |         |
| query                     | ([QueryCustomization](#querycustomization)) | アクセス先ごとにクエリを上書き/削除したい場合の設定           | -                           |         |
| proxy                     | (string)                                    | プロキシ :fa-exclamation-triangle:                            | `proxy-host`                |         |
| default_response_encoding | (string)                                    | レスポンスのエンコーディングが不明な場合の値 :fa-info-circle: | utf8                        |         |


!!! warning  "proxy"

    スキーム(`http://`など)は設定しないでください。  
    内部でhttpとhttpsを割り当てます。

!!! info "default_response_encoding"

    未指定の場合はレスポンスボディの中身を解析してencodingを推測します。  
    推測はボディが大きい場合にパフォーマンスが著しく劣化するので可能な限り指定して下さい。

    content-typeにcharsetが指定されていれば本パラメータは無関係です。


### QueryCustomization

| Key       | Type                 | Description                                       | Example                                   | Default |
|-----------|----------------------|---------------------------------------------------|-------------------------------------------|---------|
| overwrite | (dict[list[string]]) | 上書きクエリのkey-value :fa-exclamation-triangle: | <pre>{"a": ["v1"], "b": ["2", "3"]}</pre> |         |
| remove    | (list[string])       | 削除するクエリのリスト                            | `[id, name]`                              |         |

名前が`/i`で終わるキーはcase insensitive(大文字小文字を区別しない)になります。

!!! warning "overwrite"

    `overwrite`は既存のクエリに値を追加できません。  
    既にクエリの値が設定されている場合、それらは削除されます。


Examples
--------

### Production環境のアクセス先情報

```yml
name: Production
host: "http://jumeaux/production"
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

### `proxy-host`をプロキシとしてい経由するProduction環境のアクセス先情報

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

