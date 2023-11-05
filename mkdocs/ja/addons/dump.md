dump [:fontawesome-brands-github:][dump]
========================

[dump]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump

APIレスポンスを保存前に加工します。


[:fontawesome-brands-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/json.py

レスポンスがJSONの場合にJSON形式でフォーマットします。

* インデント(4)
* 改行

!!! warning "プロパティの順番について"

    プロパティの順番はソートされます。


### Config

#### Definitions

| Key              | Type     | Description                                                            | Example | Default |
|------------------|----------|------------------------------------------------------------------------|---------|---------|
| default_encoding | (string) | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |
| force            | (bool)   | typeがjson以外の場合も強制的に変換するか                               | true    | false   |


#### Examples

##### JSON形式でフォーマットする

```yaml
  dump:
    - name: json
```

##### JSON形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yaml
  dump:
    - name: json
      config:
        default_encoding: euc-jp
```

##### typeに関わらずJSON形式でフォーマットする

```yaml
  dump:
    - name: json
      config:
        force: True
```


[:fontawesome-brands-github:][xml] xml
-----------------------

[xml]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/xml.py

レスポンスがXMLの場合にXML形式でフォーマットします。

* インデント(4)
* 改行


### Config

#### Definitions

| Key              | Type     | Description                                                            | Example | Default |
|------------------|----------|------------------------------------------------------------------------|---------|---------|
| default_encoding | (string) | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |
| force            | (bool)   | typeがxml以外の場合も強制的に変換するか                                | true    | false   |


#### Examples

##### XML形式でフォーマットする

```yaml
  dump:
    - name: xml
```

##### XML形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yaml
  dump:
    - name: xml
      config:
        default_encoding: euc-jp
```

##### typeに関わらずXML形式でフォーマットする

```yaml
  dump:
    - name: xml
      config:
        force: True
```


[:fontawesome-brands-github:][html] html
-------------------------

[html]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/html.py

レスポンスをHTML形式でフォーマットします。

* インデント(1)
* 改行


### Config

#### Definitions

| Key              | Type     | Description                                                            | Example | Default |
|------------------|----------|------------------------------------------------------------------------|---------|---------|
| default_encoding | (string) | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |
| force            | (bool)   | typeがhtml以外の場合も強制的に変換するか                               | true    | false   |


#### Examples

##### HTML形式でフォーマットする

```yaml
  dump:
    - name: html
```

##### HTML形式でフォーマットする (エンコーディング情報が無ければEUC-JPで出力する)

```yaml
  dump:
    - name: html
      config:
        default_encoding: euc-jp
```

#### typeに関わらずHTML形式でフォーマットする

```yaml
  dump:
    - name: html
      config:
        force: True
```


[:fontawesome-brands-github:][encoding] encoding
--------------------------------

[encoding]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/dump/encoding.py

レスポンスのエンコーディングを変換します。


### Config

#### Definitions

|   Key    |  Type  |       Description        | Example | Default |
| -------- | ------ | ------------------------ | ------- | ------- |
| encoding | string | 変換後のエンコーディング | euc-jp  |         |


#### Examples

##### UTF8に変換する

```yaml
  dump:
    - name: encoding
```
