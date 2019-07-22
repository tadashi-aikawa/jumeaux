log2reqs [:fa-github:][s1]
==========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs

任意のFormatで記載されたリクエストを、Jumeaux内部で使用する形式([Request])に変換します。


[:fa-github:][s2] plain
-----------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/plain.py

最もシンプルな入力形式に対応しています。  
要件が単純な場合に適しています。

### Input file format

各行にリクエストURLのpathとqueryを記載します。

```
/api/path
/api/path2?key=hoge
```

!!! warning

    * pathとquery以外のパラメータは設定できません
    * GET以外のHTTPメソッドは使えません


### Config

#### Definitions

| Key                                           | Type       | Description                              | Example                     | Default |
|-----------------------------------------------|------------|------------------------------------------|-----------------------------|---------|
| encoding                                      | (string)   | 読みこみファイルのエンコーディング       | euc-jp                      | utf-8   |
| keep_blank                                    | (bool)     | 値が指定されていないクエリを有効にするか | true                        | false   |
| candidate_for_url_encodings  :fa-info-circle: | (string[]) | URLエンコーディングの候補                | <pre>- sjis<br>- euc-jp</pre> |         |

??? info "candidate_for_url_encodings"

    * 配列で指定した順番にdecodeを行い、初めに成功したエンコーディングを採用します
    * いずれのエンコーディングでもdecodeできなかった場合はutf-8になります


#### Examples

##### 最もシンプルな例

```yml
  log2reqs:
    name: plain
```

##### 入力ファイルのエンコーディングはEUC-JPで空のクエリも有効にする

```yml
  log2reqs:
    name: plain
    config:
      encoding: euc-jp
      keep_blank: true
```

##### URLエンコーディングをsjis => euc-jpの順番で推測(判定)する

```yml
  log2reqs:
    name: plain
    config:
      candidate_for_url_encodings:
        - sjis
        - euc-jp
```


[:fa-github:][s3] csv
---------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/csv.py

CSV入力形式に対応しています。
ほぼ全ての項目を指定することができます。


### Input file format

#### Definitions

| Col |            Type             | Description  |       Example       |
| --- | --------------------------- | ------------ | ------------------- |
| 1   | (string)                    | 名前         | ex1                 |
| 2   | HttpMethod :fa-info-circle: | HTTPメソッド | POST                |
| 3   | string                      | path         | /api                |
| 4   | (string)                    | query        | a=1&b=2             |
| 5   | (string)                    | header       | header1=1&header2=2 |

??? info "HttpMethod"

    --8<--
    ja/constants/http_method.md
    --8<--


#### Examples

```csv
"title1","GET","/path1","a=1&b=2","header1=1&header2=2"
"title2","GET","/path2","c=1"
"title3","GET","/path3",,"header1=1&header2=2"
"title4","GET","/path4"
```

!!! info

    後方のカラムは省略することができます

!!! warning

    * POSTのBodyを指定することはできません
    * 将来的に後方カラムの省略不可にして、POSTのBodyを指定可能にするかもしれません


### Config

#### Definitions

| Key        | Type     | Description                              | Example   | Default |
|------------|----------|------------------------------------------|-----------|---------|
| encoding   | (string) | 読みこみファイルのエンコーディング       | euc-jp    | utf-8   |
| keep_blank | (bool)   | 値が指定されていないクエリを有効にするか | true      | false   |
| dialect    | (string) | csv読みこみの方言 :fa-info-circle:       | excel-tab | excel   |

??? info "dialectの有効値"

    * excel
    * excel-tab
    * unix


#### Examples

##### 最もシンプルな例

```yml
  log2reqs:
    name: csv
```

##### 入力ファイルはtab区切りのcsvでエンコーディングはEUC-JP、空のクエリも有効にする

```yml
  log2reqs:
    name: csv
    config:
      encoding: euc-jp
      keep_blank: true
      dialect: excel-tab
```


[:fa-github:][s4] json
----------------------

[s4]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/json.py

JSON入力形式に対応しています。
全ての項目を指定することができます。

### Input file format

#### Definitions

[Request]で定義されたものをjson形式で指定できます。


#### Examples

```json
[
    {
        "path": "/users"
    },
    {
        "path": "/users",
        "method": "GET",
        "qs": {
            "id": ["147"]
        }
    },
    {
        "path": "/users",
        "method": "POST",
        "form": {"ids":["100", "200"]},
        "qs": {
            "name": ["auto"],
            "options": ["man", "japanese"]
        }
    },
    {
        "path": "/users",
        "method": "POST",
        "json": {"users": [{"id": "100", "name": "hyaku"}, {"id": "200", "name": "nihyaku"}]},
        "headers": {
            "auth-id": "xxxxxxxx",
            "device": "ios"
        }
    }
]
```


### config

#### Definitions

|   Key    |   Type   |            Description             | Example | Default |
| -------- | -------- | ---------------------------------- | ------- | ------- |
| encoding | (string) | 読みこみファイルのエンコーディング | euc-jp  | utf-8   |

#### Examples

##### 最もシンプルな例

```yml
  log2reqs:
    name: json
```

##### 入力ファイルのエンコーディングはEUC-JP

```yml
  log2reqs:
    name: json
    config:
      encoding: euc-jp
```


[:fa-github:][s5] yaml
----------------------

[s5]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/yaml.py

YAML入力形式に対応しています。
全ての項目を指定することができます。


### Input file format

#### Definitions

[Request]で定義されたものをyaml形式で指定できます。


#### Examples

```yml
- path: "/users"
- path: "/users"
  method: GET
  qs: 
    id: 
      - 147
- path: "/users"
  method: POST
  form: 
    ids: 
      - 100
      - 200
  qs: 
    name: 
      - auto
    options: 
      - man
      - japanese
- path: "/users"
  method: POST
  json: {"users": [{"id": "100", "name": "hyaku"}, {"id": "200", "name": "nihyaku"}]}
  headers: 
    "auth-id": xxxxxxxx
    device: ios
```


### config

#### Definitions

|   Key    |   Type   |            Description             | Example | Default |
| -------- | -------- | ---------------------------------- | ------- | ------- |
| encoding | (string) | 読みこみファイルのエンコーディング | euc-jp  | utf-8   |

#### Examples

##### 最もシンプルな例

```yml
  log2reqs:
    name: yaml
```

##### 入力ファイルのエンコーディングはEUC-JP

```yml
  log2reqs:
    name: yaml
    config:
      encoding: euc-jp
```

[request]: ../../models/request
