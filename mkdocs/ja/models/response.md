Response
========

responseの定義です。  
テストの結果ではなくAPIにリクエストした結果です。


Definitions
-----------

### Response

| Key          | Type           | Description                                        | Example                                   |
|--------------|----------------|----------------------------------------------------|-------------------------------------------|
| body         | bytes          | レスポンスボディのバイナリ                         | -                                         |
| status_code  | int            | レスポンスのステータスコード                       | 200                                       |
| url          | string         | リクエストしたURL                                  | http://hoge?id=1                          |
| type         | string         | レスポンス形式                                     | html, json, png など                      |
| encoding     | (string)       | 様々な情報から決定したレスポンスエンコーディング   | euc-jp                                    |
| response_sec | float          | レスポンスタイム(秒)(小数点第二位)                 | 10.23                                     |
| text         | string         | レスポンス文字列のUnicode(文字列で表せる場合)      | <pre>{"id": 1, "name": "たろう"}</pre>    |
| headers      | (dict[string]) | レスポンスヘッダ                                   | <pre>{"content-type": "text/html;"}</pre> |
| content_type | (string)       | レスポンスヘッダcontent-typeの値                   | <pre>text/html;charset=UTF-8</pre>        |
| mime_type    | (string)       | レスポンスヘッダcontent-typeに記載されたMIMEタイプ | `text/html`                               |
| charset      | (string)       | レスポンスヘッダcontent-typeに記載されたcharset    | `charset=UTF-8`                           |

