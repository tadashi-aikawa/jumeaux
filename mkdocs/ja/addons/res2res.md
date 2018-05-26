res2res [:fa-github:][s1]
=========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res

APIから返却されたレスポンスを判定前に変換します。


[:fa-github:][json] json
------------------------

[json]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res/json.py

レスポンスをJSONに変換します。  
任意の変換ロジックを指定することができます。


### Config

#### Definitions

##### Root

| Key              | Type                        | Description                                                            | Example | Default |
|------------------|-----------------------------|------------------------------------------------------------------------|---------|---------|
| transformer      | [Transformer](#transformer) | 変換処理                                                               |         |         |
| default_encoding | (string)                    | レスポンスヘッダにエンコーディング情報が無い場合の出力エンコーディング | euc-jp  | utf8    |


##### Transformer

| Key      | Type                      | Description                    | Example       | Default   |
|----------|---------------------------|--------------------------------|---------------|-----------|
| module   | string                    | 変換処理のあるモジュールのパス | sample.module |           |
| function | (string) :fa-info-circle: | 変換処理の関数                 | bytes2json    | transform |

!!! info "functionのインタフェース"

    functionで指定した関数のインタフェースは`(bytes, str) -> str`となる必要があります。  
    以下は実装の一例です。

    ```python
    def transform(anything: bytes, encoding: str) -> str:
        return json.dumps({
            "wrap": load_json(anything.decode(encoding))
        }, ensure_ascii=False)
    ```

#### Examples

##### `sample`モジュールの`transform`関数を使ってjsonに変換する

```yml
res2res:
  - name: json
    config:
      transformer:
        module: sample
```

##### `sample`モジュールの`bytes2json`関数を使ってjsonに変換する

```yml
res2res:
  - name: json
    config:
      transformer:
        module: sample
        function: bytes2json
```


[:fa-github:][json-sort] json_sort
----------------------------------

[json-sort]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res/json_sort.py

JSONレスポンスの並び順をソートします。

!!! warning "処理がスキップされるケース"

    `content-type` が `text/json` や `application/json` でない場合はレスポンスがJSONでないとみなされ処理がスキップされます。


### Config

#### Definitions

##### Root

|       Key        |        Type         |                    Description                     | Example | Default |
| ---------------- | ------------------- | -------------------------------------------------- | ------- | ------- |
| items            | [Sorter[]](#sorter) | ソート設定のリスト                                 |         |         |


##### Sorter

|    Key     |                  Type                   |             Description              | Example | Default |
| ---------- | --------------------------------------- | ------------------------------------ | ------- | ------- |
| conditions | [RequestCondition[]][request-condition] | 本設定を反映させるRequestの条件      |         |         |
| and_or     | (AndOr) :fa-info-circle:                | conditionsをAND/ORどちらで判定するか |         | and     |
| negative   | (bool)                                  | 否定条件とするか                     | true    | false   |
| targets    | [Target[]](#target)                     |                                      |         |         |

??? info "AndOr"

    --8<--
    ja/constants/and_or.md
    --8<--

##### Target

|    Key    |    Type    |                            Description                             |         Example          |     Default      |
| --------- | ---------- | ------------------------------------------------------------------ | ------------------------ | ---------------- |
| path      | string     | ソート対象となるプロパティの正規表現                               | root<'dict1'><'list1-1'> |                  |
| sort_keys | (string[]) | pathで指定したプロパティがObjectだった場合のソートプロパティリスト | `[id, name]`             | :fa-info-circle: |

!!! info "`sort_keys`が未指定の場合"

    指定プロパティの値でソートします。Objectの場合はJson Encodeした結果でソートします。

#### Examples

##### pathが`/filter`である場合 `dict1.list1-1` のリストをソートする

```yml
res2res:
  - name: json_sort
    config:
      items:
        - conditions:
            - path:
                items:
                  - regexp: /filter
          targets:
            - path: root<'dict1'><'list1-1'> 
```

##### pathが`/filter`である場合 `list2` のリストをid, nameの優先順にソートする

```yml
res2res:
  - name: json_sort
    config:
      items:
        - conditions:
            - path:
                items:
                  - regexp: /filter
          targets:
            - path: root<'list2'>
              sort_keys: [id, name]
```


[:fa-github:][type] type
------------------------

[type]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res/type.py

レスポンスのtypeを変更します。  
typeはJumeauxのアドオンや連携先アプリケーションでファイル形式を判定するために使用されます。

### Config

#### Definitions

##### Root

| Key        | Type                      | Description  | Example | Default |
|------------|---------------------------|--------------|---------|---------|
| conditions | [Condition[]](#condition) | 変更値と条件 |         |         |

##### Condition

| Key  | Type | Description                                   | Example                             | Default |
|------|------|-----------------------------------------------|-------------------------------------|---------|
| type | str  | 変更後のtype                                  | json                                |         |
| when | str  | [jinja2の式]に準拠した条件式 :fa-info-circle: | <pre>"res.status_code == 200"</pre> |         |

[jinja2の式]: http://jinja.pocoo.org/docs/2.10/templates/#expressions

!!! info "whenで指定できるプロパティ"

    | key | Description |
    |-----|-------------|
    | req | [request]   |
    | res | [response]  |


#### Examples

##### pathに`target`という文字列が含まれる場合に`json`へtypeを変更する

```yml
res2res:
  - name: type
    config:
      conditions:
        - type: json
          when: "'target' in req.path"
```

[request-condition]: /ja/models/request-condition
[request]: /ja/models/request
[response]: /ja/models/response
