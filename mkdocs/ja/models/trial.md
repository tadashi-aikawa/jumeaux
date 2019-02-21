Trial
=====

Trialの定義です。  
リクエスト1つあたりにつき1つ紐づく情報です。


Definitions
-----------

### Trial

| Key                | Type                                           | Description                                 | Example                                   |
|--------------------|------------------------------------------------|---------------------------------------------|-------------------------------------------|
| seq                | int                                            | リクエストされた順番                        | 1                                         |
| name               | string                                         | リクエストの名称(未指定の場合は`seq`と同じ) | testcase-1                                |
| tags               | string[]                                       | タグ                                        | `[good, bad]`                             |
| headers            | dict[string]                                   | レスポンスヘッダ                            | <pre>{"content-type": "text/html;"}</pre> |
| queries            | dict[string[]]                                 | リクエストのクエリ                          | a: [1]<br>b: [2]                          |
| one                | [ResponseSummary](#responsesummary)            | oneのレスポンス概要                         |                                           |
| other              | [ResponseSummary](#responsesummary)            | otherのレスポンス概要                       |                                           |
| path               | string                                         | リクエストURLのパス                         | /path                                     |
| request_time       | string                                         | リクエストした時間                          | 2018-12-03T00:12:02.444940+09:00          |
| status             | Status :fa-info-circle:                        | ステータス                                  | different                                 |  |
| diffs_by_cognition | (dict[[DiffKeys](#diffkeys)]) :fa-info-circle: | 認識と差分のあるプロパティの紐付け          |                                           |

??? info "Status"

    --8<--
    ja/constants/status.md
    --8<--

!!! info "diffs_by_cognition"

    キーは[judgement]のignoreやignore_propertiesアドオンで指定されたtitleになります。  
    どれにも当てはまらない場合は`unknown`になります。

### ResponseSummary

| Key          | Type     | Description                                        | Example                            |
|--------------|----------|----------------------------------------------------|------------------------------------|
| url          | string   | リクエストしたURL                                  | http://hoge?id=1                   |
| type         | string   | レスポンス形式                                     | html, json, png など               |
| status_code  | (int)    | レスポンスのステータスコード                       | 200                                |
| byte         | (int)    | レスポンスのバイト数                               | 123                                |
| response_sec | (float)  | レスポンスタイム(秒)(小数点第二位)                 | 10.23                              |
| content_type | (string) | レスポンスヘッダcontent-typeの値                   | <pre>text/html;charset=UTF-8</pre> |
| mime_type    | (string) | レスポンスヘッダcontent-typeに記載されたMIMEタイプ | `text/html`                        |
| encoding     | (string) | 様々な情報から決定したレスポンスエンコーディング   | euc-jp                             |
| file         | (string) | 保存されたレスポンスのファイル名                   | res1.json                          |
| prop_file    | (string) | 保存されたレスポンスプロパティのファイル名         | res1.json                          |

### DiffKeys

| Key     | Type     | Description          | Example          |
|---------|----------|----------------------|------------------|
| added   | string[] | 追加されたプロパティ | `[<root><"id">]` |
| changed | string[] | 変更されたプロパティ | `[<root><"id">]` |
| removed | string[] | 削除されたプロパティ | `[<root><"id">]` |


[judgement]: ../../addons/judgement

