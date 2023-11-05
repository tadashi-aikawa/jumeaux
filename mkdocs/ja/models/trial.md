Trial
=====

Trialの定義です。  
リクエスト1つあたりにつき1つ紐づく情報です。


Definitions
-----------

### Trial

| Key                | Type                                           | Description                                 | Example                                   |
| ------------------ | ---------------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| seq                | int                                            | リクエストされた順番                        | 1                                         |
| name               | string                                         | リクエストの名称(未指定の場合は`seq`と同じ) | testcase-1                                |
| tags               | string[]                                       | タグ                                        | `[good, bad]`                             |
| headers            | dict[string]                                   | レスポンスヘッダ                            | <pre>{"content-type": "text/html;"}</pre> |
| queries            | dict[string[]]                                 | リクエストのクエリ                          | a: [1]<br>b: [2]                          |
| raw                | (string)                                       | rawのBODY                                   | a=100&b=200                               |
| form               | (dict[string[]])                               | `x-www-form-urlencoded`のBODY               | key: [value1, value2]                     |
| json               | (dict)                                         | `applicaton/json`のBODY                     | `{id: 1, name: 'Ichi'}`                   |
| one                | [ResponseSummary](#responsesummary)            | oneのレスポンス概要                         |                                           |
| other              | [ResponseSummary](#responsesummary)            | otherのレスポンス概要                       |                                           |
| method             | HttpMethod :fontawesome-solid-circle-exclamation:                    | HTTPメソッド                                | POST                                      |
| path               | string                                         | リクエストURLのパス                         | /path                                     |
| request_time       | string                                         | リクエストした時間                          | 2018-12-03T00:12:02.444940+09:00          |
| status             | Status :fontawesome-solid-circle-exclamation:                        | ステータス                                  | different                                 |
| diffs_by_cognition | (dict[[DiffKeys](#diffkeys)]) :fontawesome-solid-circle-exclamation: | 認識と差分のあるプロパティの紐付け          |                                           |


??? info "HttpMethod"

    --8<--
    ja/constants/http_method.md
    --8<--

??? info "Status"

    --8<--
    ja/constants/status.md
    --8<--

!!! info "diffs_by_cognition"

    キーは[judgement/ignore]アドオンで指定されたtitleになります。  
    どれにも当てはまらない場合は`unknown`になります。

### ResponseSummary

| Key          | Type           | Description                                        | Example                                   |
| ------------ | -------------- | -------------------------------------------------- | ----------------------------------------- |
| url          | string         | リクエストしたURL                                  | http://hoge?id=1                          |
| type         | string         | レスポンス形式                                     | html, json, png など                      |
| status_code  | (int)          | レスポンスのステータスコード                       | 200                                       |
| byte         | (int)          | レスポンスのバイト数                               | 123                                       |
| response_sec | (float)        | レスポンスタイム(秒)(小数点第二位)                 | 10.23                                     |
| content_type | (string)       | レスポンスヘッダcontent-typeの値                   | <pre>text/html;charset=UTF-8</pre>        |
| mime_type    | (string)       | レスポンスヘッダcontent-typeに記載されたMIMEタイプ | `text/html`                               |
| encoding     | (string)       | 様々な情報から決定したレスポンスエンコーディング   | euc-jp                                    |
| file         | (string)       | 保存されたレスポンスのファイル名                   | res1.json                                 |
| prop_file    | (string)       | 保存されたレスポンスプロパティのファイル名         | res1.json                                 |
| headers      | (dict[string]) | レスポンスヘッダ  :fontawesome-solid-circle-exclamation:                 | <pre>{"content-type": "text/html;"}</pre> |



!!! info "headers"

    [judge_response_header]が`true`の場合のみ

    [judge_response_header]: ../../getstarted/configuration#Config


### DiffKeys

| Key     | Type     | Description          | Example          |
|---------|----------|----------------------|------------------|
| added   | string[] | 追加されたプロパティ | `[<root><"id">]` |
| changed | string[] | 変更されたプロパティ | `[<root><"id">]` |
| removed | string[] | 削除されたプロパティ | `[<root><"id">]` |


[judgement/ignore]: ../../addons/judgement#ignore

