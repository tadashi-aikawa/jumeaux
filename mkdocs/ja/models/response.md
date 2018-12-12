Response
========

responseの定義です。  
テストの結果ではなくAPIにリクエストした結果です。


Definitions
-----------

### Response

| Key         | Type           | Description                                      | Example                                   |
|-------------|----------------|--------------------------------------------------|-------------------------------------------|
| body        | bytes          | レスポンスボディのバイナリ                       | -                                         |
| status_code | int            | レスポンスのステータスコード                     | 200                                       |
| url         | string         | リクエストしたURL                                | http://hoge?id=1                          |
| type        | string         | レスポンス形式                                   | html, json, png など                      |
| encoding    | (string)       | 様々な情報から決定したレスポンスエンコーディング | euc-jp                                    |
| elasped_sec | float          | レスポンスタイム(秒)(小数点第二位)               | 10.23                                     |
| headers     | (dict[string]) | レスポンスヘッダ                                 | <pre>{"content-type": "text/html;"}</pre> |

