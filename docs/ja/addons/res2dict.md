res2dict [:fa-github:][s1]
==========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict

APIレスポンスを差分比較に必要なdictへ変換します。


json  [:fa-github:][s2]
-----------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/json.py

JSONレスポンスをdictに変換します。


### Config

#### Definitions

|      Key       |   Type   |                             Description                              | Example | Default |
| -------------- | -------- | -------------------------------------------------------------------- | ------- | ------- |
| force          | (bool)   | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true    | false   |
| force_encoding | (string) | レスポンスヘッダを無視してエンコーディングを強制する                 | euc-jp  |         |

??? info "`force` 変換する必要がないケース"

    * `content-type` が `text/json` や `application/json` でない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがJSONの場合 dictに変換する

```yml
- name: jumeaux.addons.res2dict.json
```

##### レスポンスをEUC-JPと決めつけて dictに変換する

```yml
- name: jumeaux.addons.res2dict.json
  config:
    force_encoding: euc-jp
```

##### 変換する必要がないケースでも強制的に変換する

```yml
- name: jumeaux.addons.res2dict.json
  config:
    force: True
```


xml  [:fa-github:][s3]
----------------------

[s3]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2dict/xml.py

XMLレスポンスをdictに変換します。


### Config

#### Definitions

|      Key       |   Type   |                             Description                              | Example | Default |
| -------------- | -------- | -------------------------------------------------------------------- | ------- | ------- |
| force          | (bool)   | 変換する必要がないケース :fa-info-circle: でも強制的に変換するか | true    | false   |
| force_encoding | (string) | レスポンスヘッダを無視してエンコーディングを強制する                 | euc-jp  |         |

??? info "`force` 変換する必要がないケース"

    * `content-type` が `text/xml` や `application/xml` でない場合
    * 既にアドオンでdict型に変換済みの場合


#### Examples

##### レスポンスがXMLの場合 dictに変換する

```yml
- name: jumeaux.addons.res2dict.xml
```

##### レスポンスをEUC-JPと決めつけて dictに変換する

```yml
- name: jumeaux.addons.res2dict.xml
  config:
    force_encoding: euc-jp
```

##### 変換する必要がないケースでも強制的に変換する

```yml
- name: jumeaux.addons.res2dict.xml
  config:
    force: True
```
