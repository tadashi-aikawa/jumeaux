log2reqs [:fa-github:][s1]
==========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs

任意のFormatで記載されたリクエストを、Jumeaux内部で使用する形式(Request型)に変換します。


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

    pathとquery以外のパラメータは設定できません


### Config

#### Definitions

|   Key    |   Type   |            Description             | Example | Default |
| -------- | -------- | ---------------------------------- | ------- | ------- |
| encoding | (string) | 読みこみファイルのエンコーディング | euc-jp  | utf-8   |


#### Examples

##### 最もシンプルな例

```yml
log2reqs:
  name: plain
```

##### 入力ファイルのエンコーディングはEUC-JP

```yml
log2reqs:
  name: plain
  config:
    encoding: euc-jp
```


[:fa-github:][s3] csv
---------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/csv.py

CSV入力形式に対応しています。
ほぼ全ての項目を指定することができます。


### Input file format

#### Definitions

| Col |   Type   | Description |       Example       |
| --- | -------- | ----------- | ------------------- |
| 1   | (string) | 名前        | ex1                 |
| 2   | string   | path        | /api                |
| 3   | (string) | query       | a=1&b=2             |
| 4   | (string) | header      | header1=1&header2=2 |

#### Examples

```csv
"title1","/path1","a=1&b=2","header1=1&header2=2"
"title2","/path2","c=1"
"title3","/path3",,"header1=1&header2=2"
"title4","/path4"
```

!!! info

    後方のカラムは省略することができます


### Config

#### Definitions

|   Key    |   Type   |            Description             |  Example  | Default |
| -------- | -------- | ---------------------------------- | --------- | ------- |
| encoding | (string) | 読みこみファイルのエンコーディング | euc-jp    | utf-8   |
| dialect  | (string) | csv読みこみの方言 :fa-info-circle: | excel-tab | excel   |

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

##### 入力ファイルはtab区切りのcsvでエンコーディングはEUC-JP

```yml
log2reqs:
  name: csv
  config:
    encoding: euc-jp
    dialect: excel-tab
```


[:fa-github:][s4] json
----------------------

[s4]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/log2reqs/json.py

JSON入力形式に対応しています。
全ての項目を指定することができます。

### Input file format

#### Definitions

|   Key   |     Type     | Description |            Example             | Default |
| ------- | ------------ | ----------- | ------------------------------ | ------- |
| name    | (string)     | 名前        | title                          |         |
| path    | string       | path        | /api                           |         |
| qs      | (dict[list]) | query       | `{"a": [1], "b": [2, 3]}`      |         |
| headers | (dict)       | header      | `{"header1": 1, "header2": 2}` |         |


#### Examples

```json
[
    {
        "name": "title1",
        "path": "/api1",
        "qs": {
            "a": [1],
            "b": [2, 3]
        },
        "header": {
            "header1": 1,
            "header2": 2
        }
    },
    {
        "path": "/api2"
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


|   Key   |     Type     | Description |         Example          | Default |
| ------- | ------------ | ----------- | ------------------------ | ------- |
| name    | (string)     | 名前        | title                    |         |
| path    | string       | path        | /api                     |         |
| qs      | (dict[list]) | query       | a: [1]<br>b: [2]         |         |
| headers | (dict)       | header      | header1: 1<br>header2: 2 |         |


#### Examples

```yml
- name: title1
  path: /api1
  qs:
    a: [1]
    b: [2, 3]
  header:
    header1: 1
    header2: 2
- path: /api2
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
