AccessPoint
===========

アクセス先情報の定義です。

Definitions
-----------

### AccessPoint

| Key                       | Type     | Description                                                   | Example                     | Default |
|---------------------------|----------|---------------------------------------------------------------|-----------------------------|---------|
| name                      | string   | アクセス先の名称                                              | Production                  |         |
| host                      | string   | アクセス先のhost                                              | `http://jumeaux/production` |         |
| proxy                     | (string) | プロキシ :fa-exclamation-triangle:                            | `proxy-host`                |         |
| default_response_encoding | (string) | レスポンスのエンコーディングが不明な場合の値 :fa-info-circle: | utf8                        |         |

!!! warning  "proxy"

    スキーム(`http://`など)は設定しないでください。  
    内部でhttpとhttpsを割り当てます。

!!! info "default_response_encoding"

    未指定の場合はレスポンスボディの中身を解析してencodingを推測します。  
    推測はボディが大きい場合にパフォーマンスが著しく劣化するので可能な限り指定して下さい。

    content-typeにcharsetが指定されていれば本パラメータは無関係です。


Examples
--------

### Production環境のアクセス先情報

```yml
name: Production
host: "http://jumeaux/production"
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

