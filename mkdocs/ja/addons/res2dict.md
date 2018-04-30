res2dict [:fa-github:][res2dict]
================================

[res2dict]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict

APIレスポンスを差分比較に必要なdictへ変換します。


[:fa-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/json.py

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


[:fa-github:][xml] xml
----------------------

[xml]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/xml.py

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


[:fa-github:][html] html
------------------------

[html]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/html.py

HTMLレスポンスをdictに変換します。


### Config

#### Definitions

| Key        | Type       | Description                                                      | Example                 | Default                |
|------------|------------|------------------------------------------------------------------|-------------------------|------------------------|
| force      | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true                    | false                  |
| mime_types | (string[]) | 対応MIMEタイプ                                                   | <pre>- text/xhtml</pre> | <pre>- text/html</pre> |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがHTMLの場合 dictに変換する

```yaml
res2dict:
  - name: html
```

##### 変換する必要がないケースでも強制的に変換する

```yaml
res2dict:
  - name: html
    config:
      force: true
```

##### MIMEタイプが `text/xhtml` のときだけ変換する

```yaml
res2dict:
  - name: html
    config:
      mime_types:
        - text/xhtml
```



[:fa-github:][block] block
--------------------------

[block]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/block.py

ブロック単位(空行で区切られた)のレスポンスをdictに変換します。
ブロック単位の定義は下記セクションを参照してください。


### Config

#### Definitions

|      Key      |    Type    |                            Description                            |         Example         |         Default         |
| ------------- | ---------- | ----------------------------------------------------------------- | ----------------------- | ----------------------- |
| header_regexp | string     | ヘッダ行のキーを抽出する正規表現 :fa-exclamation-triangle:        | <pre>^\d+\)(.+)</pre>   |                         |
| record_regexp | string     | レコード行のkey/valueを抽出する正規表現 :fa-exclamation-triangle: | <pre>([^ ]+) (.+)</pre> |                         |
| force         | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか  | true                    | false                   |
| mime_types    | (string[]) | 対応MIMEタイプ                                                    | <pre>- text/xml</pre>   | <pre>- text/plain</pre> |

!!! warning "header_regexpの正規表現について"

    グループを1つ定義してください

!!! warning "record_regexpの正規表現について"

    グループを2つ定義してください. 1つ目がkey 2つ目がvalueになります

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### MIMEタイプが `text/xml` のときだけINIファイルっぽい形式に変換する

```yml
res2dict:
  - name: block
    config:
      mime_types:
        - text/xml
      header_regexp: '\[(.+)\]'
      record_regexp: '([^:]+): (.+)'
```


### ブロック単位のルール

* 1つ以上の空行で区切られた単位をブロック単位とする
* ブロックは1行のヘッダと1行以上のレコードで構成される


#### パターン1

##### 変換対象

```
[Mimizou]
ID: 001
Name: Mimizou Aikawa

[Tatsuwo(GOD)]
ID: 002
Name: Tatsuwo Aikawa
```

##### configの設定

```
header_regexp: '\[(.+)\]'
record_regexp: '([^:]+): (.+)'
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

#### パターン2

##### 変換対象

```
1)Mimizou
ID 001
Name Mimizou Aikawa

12)Tatsuwo(GOD)
ID 002
Name Tatsuwo Aikawa
```

##### configの設定

```
header_regexp: '^\d+\)(.+)'
record_regexp: '([^ ]+) (.+)'
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
