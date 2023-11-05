Request
=======

requestの定義です。

Definitions
-----------

### Request

| Key     | Type                          | Description                   | Example                  | Default |
| ------- | ----------------------------- | ----------------------------- | ------------------------ | ------- |
| path    | string                        | リクエストのPath              | /repositories            |         |
| name    | (string)                      | リクエストの名称              | request1                 |         |
| qs      | (dict[string[]])              | リクエストのクエリ            | a: [1]<br>b: [2]         | `{}`    |
| headers | (dict[string])                | リクエストヘッダ              | header1: 1<br>header2: 2 | `{}`    |
| method  | (HttpMethod) :fontawesome-solid-circle-exclamation: | HTTPメソッド                  | POST                     | GET     |
| raw     | (string)                      | `raw`のBody                   | a=100&b=200              |         |
| form    | (dict[string[]])              | `x-www-form-urlencoded`のBody | key: [value1, value2]    |         |
| json    | (dict)                        | `application/json`のBody      | `{id: 1, name: 'Ichi'}`  |         |

??? info "HttpMethod"

    --8<--
    ja/constants/http_method.md
    --8<--


Examples
--------

### `/sample/one?word=hoge&size=10` 相当の `hogehoge` という名前のリクエスト

```yaml
path: /sample/one
name: hogehoge
qs:
  word: [hoge]
  size: ["10"]
```

### `/sample/two` 相当で リクエストヘッダが `x-header="1", y-header="2"` である名も無きリクエスト

```yaml
path: /sample/two
headers:
  x-header: "1"
  y-header: "2"
```

### `/post` に content-type が `x-www-form-urlencoded` で `p1=11&p2=22` のクエリをリクエスト

```yaml
path: /post
method: POST
form:
  p1: [11]
  p2: [22]
```

### `/post` に raw string で `p1=11&p2=22` のクエリをリクエスト

```yaml
path: /post
method: POST
raw: "p1=11&p2=22"
```
