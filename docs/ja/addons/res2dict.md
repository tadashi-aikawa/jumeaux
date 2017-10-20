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

|      Key       |   Type   |                           Description                            | Example | Default |
| -------------- | -------- | ---------------------------------------------------------------- | ------- | ------- |
| force          | (bool)   | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true    | false   |

!!! info "`force` 変換する必要がないケース"

    * `content-type` が `text/json` や `application/json` でない場合
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
      force: True
```


[:fa-github:][s3] xml
---------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/xml.py

XMLレスポンスをdictに変換します。


### Config

#### Definitions

|      Key       |   Type   |                           Description                            | Example | Default |
| -------------- | -------- | ---------------------------------------------------------------- | ------- | ------- |
| force          | (bool)   | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true    | false   |

!!! info "`force` 変換する必要がないケース"

    * `content-type` が `text/xml` や `application/xml` でない場合
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
      force: True
```
