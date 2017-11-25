Request
=======

requestのの定義です。

Definitions
-----------

### Request

|   Key   |       Type       |    Description     |         Example          | Default |
| ------- | ---------------- | ------------------ | ------------------------ | ------- |
| path    | string           | リクエストのPath   | /repositories            |         |
| name    | (string)         | リクエストの名称   | request1                 |         |
| qs      | (dict[string[]]) | リクエストのクエリ | a: [1]<br>b: [2]         | `{}`    |
| headers | (dict[string])   | リクエストヘッダ   | header1: 1<br>header2: 2 | `{}`    |

Examples
--------

### `/sample/one?word=hoge&size=10` 相当の `hogehoge` という名前のリクエスト

```yml
path: /sample/one
name: hogehoge
qs:
  word: [hoge]
  size: ["10"]
```

### `/sample/two` 相当で リクエストヘッダが `x-header="1", y-header="2"` である名も無きリクエスト

```yml
path: /sample/two
headers:
  x-header: "1"
  y-header: "2"
```
