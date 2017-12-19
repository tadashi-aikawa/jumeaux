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


[:fa-github:][s3] richplain
---------------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/richplain.py

以下のような特殊な形式のレスポンスをdictに変換します。

### 特殊な形式とは

#### 変換前の形式

```
1)Mimizou
ID 001
Name Mimizou Aikawa

2)Tatsuwo(GOD)
ID 002
Name Tatsuwo Aikawa
```

#### 変換後のdict

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


### Config

#### Definitions

|    Key     |    Type    |                           Description                            |        Example        |         Default         |
| ---------- | ---------- | ---------------------------------------------------------------- | --------------------- | ----------------------- |
| force      | (bool)     | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true                  | false                   |
| mime_types | (string[]) | 対応MIMEタイプ                                                   | <pre>- text/xml</pre> | <pre>- text/plain</pre> |

!!! info "`force` 変換する必要がないケース"

    以下のいずれかに一致する場合

    * MIMEタイプ が `mime_types` のいずれにも一致しない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスが特殊形式の場合 dictに変換する

```yml
res2dict:
  - name: richplain
```

##### 変換する必要がないケースでも強制的に変換する

```yml
res2dict:
  - name: richplain
    config:
      force: true
```

##### MIMEタイプが `text/xml` のときだけ変換する

```yml
res2dict:
  - name: richplain
    config:
      mime_types:
        - text/xml
```
