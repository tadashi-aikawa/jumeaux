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

|       Key        |    Type    |                              Description                               |        Example         |                    Default                    |
| ---------------- | ---------- | ---------------------------------------------------------------------- | ---------------------- | --------------------------------------------- |
| default_encoding | (string)   | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp                 | utf8                                          |
| mime_types       | (string[]) | 対応MIMEタイプ                                                         | <pre>- text/json</pre> | <pre>- text/json<br/>- application/json</pre> |
| force            | (bool)     | MIMEタイプが未対応の場合でも強制的に変換するか                         | true                   | false                                         |


#### Examples

##### JSON形式でフォーマットする

```yml
dump:
  - name: json
```

##### JSON形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yml
dump:
  - name: json
    config:
      default_encoding: euc-jp
```

##### MIMEタイプが `application/json` の時だけJSON形式でフォーマットする

```yml
dump:
  - name: json
    config:
      mime_types:
        - application/json
```

##### MIMEタイプに関係なく JSON形式でフォーマットする

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

|       Key        |    Type    |                              Description                               |        Example        |                   Default                   |
| ---------------- | ---------- | ---------------------------------------------------------------------- | --------------------- | ------------------------------------------- |
| default_encoding | (string)   | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp                | utf8                                        |
| mime_types       | (string[]) | 対応MIMEタイプ                                                         | <pre>- text/xml</pre> | <pre>- text/xml<br/>- application/xml</pre> |
| force            | (bool)     | MIMEタイプが未対応の場合でも強制的に変換するか                         | true                  | false                                       |


#### Examples

##### XML形式でフォーマットする

```yml
dump:
  - name: xml
```

##### XML形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yml
dump:
  - name: xml
    config:
      default_encoding: euc-jp
```

##### MIMEタイプが `text/xml` の時だけXML形式でフォーマットする

```yml
dump:
  - name: xml
    config:
      mime_types:
        - text/xml
```

##### MIMEタイプに関係なく XML形式でフォーマットする

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
