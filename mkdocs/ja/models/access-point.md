AccessPoint
===========

アクセス先情報の定義です。

Definitions
-----------

### AccessPoint

|  Key  |   Type   |            Description             |           Example           | Default |
| ----- | -------- | ---------------------------------- | --------------------------- | ------- |
| name  | string   | アクセス先の名称                   | Production                  |         |
| host  | string   | アクセス先のhost                   | `http://jumeaux/production` |         |
| proxy | (string) | プロキシ :fa-exclamation-triangle: | `proxy-host`                |         |

!!! warning  "proxy"

    スキーム(`http://`など)は設定しないでください。  
    内部でhttpとhttpsを割り当てます。


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
