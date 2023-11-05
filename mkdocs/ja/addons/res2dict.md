res2dict [:fontawesome-brands-github:][res2dict]
================================

[res2dict]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict

APIレスポンスを差分比較に必要なdictへ変換します。


[:fontawesome-brands-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/json.py

JSONレスポンスをdictに変換します。  


### Config

#### Definitions

| Key   | Type   | Description                                                      | Example | Default |
|-------|--------|------------------------------------------------------------------|---------|---------|
| force | (bool) | 変換する必要がないケース :fontawesome-solid-circle-exclamation: でも強制的に変換するか | true    | false   |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * レスポンスのtypeがjsonではない
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがJSONの場合 dictに変換する

```yaml
  res2dict:
    - name: json
```

##### 変換する必要がないケースでも強制的に変換する

```yaml
  res2dict:
    - name: json
      config:
        force: true
```


[:fontawesome-brands-github:][xml] xml
----------------------

[xml]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/xml.py

XMLレスポンスをdictに変換します。


### Config

#### Definitions

| Key   | Type   | Description                                                      | Example | Default |
|-------|--------|------------------------------------------------------------------|---------|---------|
| force | (bool) | 変換する必要がないケース :fontawesome-solid-circle-exclamation: でも強制的に変換するか | true    | false   |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * レスポンスのtypeがxmlではない
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがXMLの場合 dictに変換する

```yaml
  res2dict:
    - name: xml
```

##### 変換する必要がないケースでも強制的に変換する

```yaml
  res2dict:
    - name: xml
      config:
        force: true
```


[:fontawesome-brands-github:][html] html
------------------------

[html]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/html.py

HTMLレスポンスをdictに変換します。


### Config

#### Definitions

| Key   | Type   | Description                                                      | Example | Default |
|-------|--------|------------------------------------------------------------------|---------|---------|
| force | (bool) | 変換する必要がないケース :fontawesome-solid-circle-exclamation: でも強制的に変換するか | true    | false   |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * レスポンスのtypeがhtmlではない
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


[:fontawesome-brands-github:][block] block
--------------------------

[block]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/block.py

ブロック単位(空行で区切られた)のレスポンスをdictに変換します。
ブロック単位の定義は下記セクションを参照してください。


### Config

#### Definitions

| Key           | Type   | Description                                                       | Example                 | Default |
|---------------|--------|-------------------------------------------------------------------|-------------------------|---------|
| header_regexp | string | ヘッダ行のキーを抽出する正規表現 :fontawesome-solid-triangle-exclamation:        | <pre>^\d+\)(.+)</pre>   |         |
| record_regexp | string | レコード行のkey/valueを抽出する正規表現 :fontawesome-solid-triangle-exclamation: | <pre>([^ ]+) (.+)</pre> |         |
| force         | (bool) | 変換する必要がないケース :fontawesome-solid-circle-exclamation: でも強制的に変換するか  | true                    | false   |

!!! warning "header_regexpの正規表現について"

    グループを1つ定義してください

!!! warning "record_regexpの正規表現について"

    グループを2つ定義してください. 1つ目がkey 2つ目がvalueになります

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### INIファイルっぽい形式に変換する

```yaml
  res2dict:
    - name: block
      config:
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
