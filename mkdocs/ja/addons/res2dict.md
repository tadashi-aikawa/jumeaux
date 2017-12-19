res2dict [:fa-github:][s1]
==========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict

APIレスポンスを差分比較に必要なdictへ変換します。


[:fa-github:][s2] json
----------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/json.py

JSONレスポンスをdictに変換します。


### Config

#### Definitions

|    Key     |    Type    |                           Description                            |        Example         |                    Default                    |
| ---------- | ---------- | ---------------------------------------------------------------- | ---------------------- | --------------------------------------------- |
| force      | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true                   | false                                         |
| mime_types | (string[]) | 対応MIMEタイプ                                                   | <pre>- text/json</pre> | <pre>- text/json<br/>- application/json</pre> |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがJSONの場合 dictに変換する

```yml
res2dict:
  - name: json
```

##### 変換する必要がないケースでも強制的に変換する

```yml
res2dict:
  - name: json
    config:
      force: true
```

##### MIMEタイプが `application/json` のときだけ変換する

```yml
res2dict:
  - name: json
    config:
      mime_types:
        - application/json
```


[:fa-github:][s3] xml
---------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/xml.py

XMLレスポンスをdictに変換します。


### Config

#### Definitions

|    Key     |    Type    |                           Description                            |        Example        |                   Default                   |
| ---------- | ---------- | ---------------------------------------------------------------- | --------------------- | ------------------------------------------- |
| force      | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true                  | false                                       |
| mime_types | (string[]) | 対応MIMEタイプ                                                   | <pre>- text/xml</pre> | <pre>- text/xml<br/>- application/xml</pre> |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがXMLの場合 dictに変換する

```yml
res2dict:
  - name: xml
```

##### 変換する必要がないケースでも強制的に変換する

```yml
res2dict:
  - name: xml
    config:
      force: true
```

##### MIMEタイプが `text/xml` のときだけ変換する

```yml
res2dict:
  - name: xml
    config:
      mime_types:
        - text/xml
```


[:fa-github:][s3] block
-----------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/block.py

ブロック単位(空行で区切られた)のレスポンスをdictに変換します。
ブロック単位の定義は下記セクションを参照してください。


### Config

#### Definitions

|      Key      |    Type    |                            Description                            |        Example        |         Default         |
| ------------- | ---------- | ----------------------------------------------------------------- | --------------------- | ----------------------- |
| header_regexp | (string)   | ヘッダ行のキーを抽出する正規表現 :fa-exclamation-triangle:        | `^\d+\)(.+)`          | `\[(.+)\]`              |
| record_regexp | (string)   | レコード行のkey/valueを抽出する正規表現 :fa-exclamation-triangle: | `([^ ]+) (.+)`        | `([^:]+): (.+)`         |
| force         | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか  | true                  | false                   |
| mime_types    | (string[]) | 対応MIMEタイプ                                                    | <pre>- text/xml</pre> | <pre>- text/plain</pre> |

!!! warning "header_regexpの正規表現について"

    * グループを1つ定義してください
    * yamlにダブルクォートで記載する際は`\`を`\\\\`と記載してください (yamlのルール)

!!! warning "record_regexpの正規表現について"

    * グループを2つ定義してください. 1つ目がkey 2つ目がvalueになります
    * yamlにダブルクォートで記載する際は`\`を`\\\\`と記載してください (yamlのルール)

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### MIMEタイプが `text/xml` のときだけブロック形式に変換する

```yml
res2dict:
  - name: block
    config:
      mime_types:
        - text/xml
```

##### ヘッダとレコードの正規表現を指定する

```yml
res2dict:
  - name: block
    config:
      force: true
      header_regexp: "^\\\\d+\\\\)(.+)"
      record_regexp: "([^ ]+) (.+)"
```


### ブロック単位のルール

* 1つ以上の空行で区切られた単位をブロック単位とする
* ブロックの1行目はヘッダである
* ブロックの2行目以降はレコードである

#### ヘッダとレコードの抽出条件がデフォルトの場合

##### 変換前

```
[Mimizou]
ID: 001
Name: Mimizou Aikawa

[Tatsuwo(GOD)]
ID: 002
Name: Tatsuwo Aikawa
```

##### 変換後

```
{
  "Mimizou": {
    "ID": "001",
    "Name": "Mimizou Aikawa"
  },
  "Tatsuwo(GOD)": {
    "ID": "002",
    "Name": "Tatsuwo Aikawa"
  }
}
```

#### ヘッダとレコードの抽出条件をカスタムした場合

下記のように条件を設定した場合

```
header_regexp: "^\\\\d+\\\\)(.+)"
record_regexp: "([^ ]+) (.+)"
```

##### 変換前

```
1)Mimizou
ID 001
Name Mimizou Aikawa

12)Tatsuwo(GOD)
ID 002
Name Tatsuwo Aikawa
```

##### 変換後

```
{
  "Mimizou": {
    "ID": "001",
    "Name": "Mimizou Aikawa"
  },
  "Tatsuwo(GOD)": {
    "ID": "002",
    "Name": "Tatsuwo Aikawa"
  }
}
```
