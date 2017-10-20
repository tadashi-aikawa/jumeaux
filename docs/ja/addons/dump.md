dump [:fa-github:][s1]
======================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump

APIレスポンスを保存前に加工します。


[:fa-github:][s2] json
----------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/json.py

レスポンスをJSON形式でフォーマットします。

* インデント(4)
* 改行

!!! warning "プロパティの順番について"

    プロパティの順番はソートされます。


### Config

#### Definitions

|       Key        |   Type   |                              Description                               | Example | Default |
| ---------------- | -------- | ---------------------------------------------------------------------- | ------- | ------- |
| default_encoding | (string) | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |
| force            | (bool)   | JSONでない場合 :fa-info-circle: でも強制的に変換するか                 | true    | false   |

!!! info "`force` JSONでない場合"

    `content-type` が `text/json` や `application/json` でない場合


#### Examples

##### レスポンスがJSONの場合 JSON形式でフォーマットする

```yml
dump:
  - name: json
```

##### レスポンスがJSONの場合 JSON形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yml
dump:
  - name: json
    config:
      default_encoding: euc-jp
```

##### レスポンスがJSONで無い場合も JSON形式でフォーマットする

```yml
dump:
  - name: json
    config:
      force: True
```


[:fa-github:][s3] xml
----------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/xml.py

レスポンスをXML形式でフォーマットします。

* インデント(4)
* 改行


### Config

#### Definitions

|       Key        |   Type   |                              Description                               | Example | Default |
| ---------------- | -------- | ---------------------------------------------------------------------- | ------- | ------- |
| default_encoding | (string) | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |
| force            | (bool)   | XMLでない場合 :fa-info-circle: でも強制的に変換するか                  | true    | false   |

!!! info "`force` XMLでない場合"

    `content-type` が `text/xml` や `application/xml` でない場合


#### Examples

##### レスポンスがXMLの場合 XML形式でフォーマットする

```yml
dump:
  - name: xml
```

##### レスポンスがXMLの場合 XML形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yml
dump:
  - name: xml
    config:
      default_encoding: euc-jp
```

##### レスポンスがXMLで無い場合も XML形式でフォーマットする

```yml
dump:
  - name: xml
    config:
      force: True
```


[:fa-github:][s3] encoding
--------------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/encoding.py

レスポンスのエンコーディングを変換します。


### Config

#### Definitions

|   Key    |  Type  |       Description        | Example | Default |
| -------- | ------ | ------------------------ | ------- | ------- |
| encoding | string | 変換後のエンコーディング | euc-jp  |         |


#### Examples

##### UTF8に変換する

```yml
dump:
  - name: encoding
```
