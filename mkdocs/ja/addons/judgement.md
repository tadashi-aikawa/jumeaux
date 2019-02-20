judgement [:fa-github:][s1]
===========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement

プロパティ差分情報を元に ステータス(Same/Different)を決定します。


[:fa-github:][ignore_properties] ignore_properties
--------------------------------------------------

!!! danger

    本アドオンは非推奨です。代わりに[ignore](#ignore)を使用してください。
    
[ignore_properties]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement/ignore_properties.py

以下2つの情報を生成します。

* configで指定したプロパティを無視した上で判定したステータス
* 無視したプロパティのキー と 無視するために参照した設定名

!!! warning

    既に同レイヤーのアドオンでSameと判定されている場合、本アドオンは実行されません。


### Config

#### Definitions

##### Root

| Key     | Type                      | Description | Example | Default |
|---------|---------------------------|-------------|---------|---------|
| ignores | [IgnoreOld[]](#ignoreold) | 無視設定    |         |         |

##### IgnoreOld

| Key        | Type                            | Description                     | Example                | Default |
|------------|---------------------------------|---------------------------------|------------------------|---------|
| title      | (string)                        | タイトル                        | IDは毎回変わるので無視 |         |
| conditions | [ConditionOld[]](#conditionold) | 本設定を反映させるRequestの条件 |                        |         |
| image      | (string)                        | 画像のURL                       | https://hoge.png       |         |
| link       | (string)                        | 参考URL                         | https://reference.html |         |

!!! note "`image`と`link`について"

    画像のURLと参考URLはViewerなどで利用されることを想定しています。

##### ConditionOld

|   Key   |    Type    |                                 Description                                  |                    Example                    | Default |
| ------- | ---------- | ---------------------------------------------------------------------------- | --------------------------------------------- | ------- |
| name    | (string)   | nameの正規表現 :fa-exclamation-triangle:                                     | `api.+`                                       |         |
| path    | (string)   | pathの正規表現 :fa-exclamation-triangle:                                     | `/api.*`                                      |         |
| added   | (string[]) | 追加されていても無視するプロパティの正規表現リスト :fa-exclamation-triangle: | `- root<'id'>`<br>`- root<'items'><d+><'id'>` |         |
| changed | (string[]) | 変更されていても無視するプロパティの正規表現リスト :fa-exclamation-triangle: | `- root<'id'>`<br>`- root<'items'><d+><'id'>` |         |
| removed | (string[]) | 削除されていても無視するプロパティの正規表現リスト :fa-exclamation-triangle: | `- root<'id'>`<br>`- root<'items'><d+><'id'>` |         |

!!! warning "正規表現について"

    Descriptionの正規表現は完全一致正規表現を意味します。
    例えば 完全正規表現`hoge`は`ahoge` に一致しません。

!!! warning "`added`, `changed`, `removed` コーテーションについて"

     プロパティが文字列の場合コーテーションを付けて下さい。
     また、数字の場合はコーテーションを付けないで下さい。


#### Examples

##### path `/api1` の `items[].id` は値が変更されていても無視する

```yml
  judgement:
    - name: ignore_properties
      config:
        ignores:
          - title: API1のitems[].idの値は無視
            conditions:
              - path: /api1
                changed:
                  - root<'items'><\d+><'id'>
```

##### 複雑な条件

以下2つのケースを無視した上でステータスを判断する。

* pathが ``/api`` から始まる ``id`` は追加されている倍委
* nameに ``check`` を含む ``debug`` または ``url`` は削除されている場合

```yml
  judgement:
    - name: ignore_properties
      config:
        ignores:
          - title: /apiから始まるidは無視
            conditions:
              - path: /api.*
                added:
                  - root<'id'>
          - title: タイトルにcheckを含む場合は全階層のdebugとurlを無視
            conditions:
              - name: .*check.*
                image: http://hoge.png
                link: http://hoge.html
                removed:
                  - .*<'(debug|url)'>.*
```


[:fa-github:][_ignore] ignore
-----------------------------

[_ignore]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement/ignore.py

以下2つの情報を生成します。

* configで指定したプロパティを無視した上で判定したステータス
* 無視したプロパティのキー と 無視するために参照した設定名

!!! warning

    既に同レイヤーのアドオンでSameと判定されている場合、本アドオンは実行されません。


### Config

#### Definitions

##### Root

| Key     | Type                 | Description | Example | Default |
|---------|----------------------|-------------|---------|---------|
| ignores | [Ignore[]](#ignore_) | 無視設定    |         |         |


##### <a name="ignore_" style="padding-top: 70px; margin-top: -70px;"></a>Ignore

|    Key     |           Type            |           Description           |        Example         | Default |
| ---------- | ------------------------- | ------------------------------- | ---------------------- | ------- |
| title      | (string)                  | タイトル                        | IDは毎回変わるので無視 |         |
| conditions | [Condition[]](#condition) | 本設定を反映させるRequestの条件 |                        |         |

!!! note "`title`について"

    titleが同じものは同一条件として扱われます。

##### Condition

| Key     | Type              | Description                                      | Example                          | Default |
|---------|-------------------|--------------------------------------------------|----------------------------------|---------|
| when    | (string)          | 条件式 :fa-exclamation-triangle:                 | <pre>"req.path == '/test'"</pre> |         |
| added   | ([Case[]](#case)) | 追加されていても無視するプロパティのリストと条件 |                                  |         |
| changed | ([Case[]](#case)) | 変更されていても無視するプロパティのリストと条件 |                                  |         |
| removed | ([Case[]](#case)) | 削除されていても無視するプロパティのリストと条件 |                                  |         |


??? info "whenについて"

    [Template表記]に対応しています。
    プロパティは以下を使用できます。

    | key        | Type                 | Description           |
    |------------|----------------------|-----------------------|
    | req        | [Request][request]   | リクエスト情報        |
    | res_one    | [Response][response] | oneのレスポンス情報   |
    | res_other  | [Response][response] | otherのレスポンス情報 |
    | dict_one   | (dict)               | oneのプロパティ情報   |
    | dict_other | (dict)               | otherのプロパティ情報 |

    whenが指定されなかった場合は全て条件に一致したとみなします。


##### Case

| Key  | Type   | Description                    | Example                                | Default |
|------|--------|--------------------------------|----------------------------------------|---------|
| path | string | プロパティの正規表現(完全一致) | `root<'id'>` :fa-exclamation-triangle: |         |
| when | (str)  | 条件式 :fa-info-circle:        | <pre>"one.name == 'hoge'"</pre>        |         |


??? info "whenについて"

    [Template表記]に対応しています。
    プロパティは以下を使用できます。

    | key   | Type  | Description                                   |
    |-------|-------|-----------------------------------------------|
    | one   | (any) | oneのpathで指定したプロパティに入っている値   |
    | other | (any) | otherのpathで指定したプロパティに入っている値 |

    * `added`の場合はoneが`None`
    * `removed`の場合はotherが`None`

    whenが指定されなかった場合は全て条件に一致したとみなします。


!!! warning "pathのコーテーションについて"

    プロパティが文字列の場合コーテーションを付けて下さい。
    数字の場合はコーテーションを付けないで下さい。


#### Examples

##### path `/api1` の `items[].id` は値が変更されていても無視する

```yml
  judgement:
    - name: ignore
      config:
        ignores:
          - title: API1のitems[].idの値は無視
            conditions:
              - when: 'req.path == "/api1"'
                changed:
                  - path: root<'items'><\d+><'id'>
```

##### `items[].type` が追加されていても、その値がallなら無視する

```yml
  judgement:
    - name: ignore
      config:
        ignores:
          - title: items[].type
            conditions:
              - added:
                  - path: root<'items'><\d+><'type'>
                    when: 'other == "all"'
```

##### 複雑な条件

以下3つのケースを無視した上でステータスを判断する。

* pathが ``/api`` から始まる場合に追加された ``.id``
* nameに ``check`` を含む ``debug`` または ``url`` は削除されている場合
* ``name`` がignoreまたはunknown に変更された場合

```yml
  judgement:
    - name: ignore_properties
      config:
        ignores:
          - title: /apiから始まる場合に追加されたプロパティ.idは無視
            conditions:
              - when: 'req.path|reg("/api.*")'
                added:
                  - path: root<'id'>
          - title: nameにcheckを含む場合は全階層のプロパティdebugとurlが削除されていても無視
            conditions:
              - when: 'req.name|reg(.*check.*)'
                removed:
                  - path: .*<'(debug|url)'>.*
          - title: プロパティ.nameがignoreまたはunknownに変更された場合だけは無視
            conditions:
              - changed:
                  - path: root<'name'>
                    when: 'other in ["ignore", "unknown"]'
```


[:fa-github:][same] same
------------------------

[same]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement/same.py

指定した条件のいずれかに一致する場合、ステータスをSameにします。


### Config

#### Definitions

##### Root

| Key      | Type  | Description             | Example                      | Default |
|----------|-------|-------------------------|------------------------------|---------|
| when_any | str[] | 条件式 :fa-info-circle: | <pre>'"2" in req.path'</pre> |         |


??? info "when_anyで指定できるプロパティ"

    [Template表記]に対応しています。
    プロパティは以下を使用できます。

    | key        | Type                 | Description           |
    |------------|----------------------|-----------------------|
    | req        | [Request][request]   | リクエスト情報        |
    | res_one    | [Response][response] | oneのレスポンス情報   |
    | res_other  | [Response][response] | otherのレスポンス情報 |
    | dict_one   | (dict)               | oneのプロパティ情報   |
    | dict_other | (dict)               | otherのプロパティ情報 |


#### Examples

##### リクエストのpathが`/test0`または`/test1`のときはSameとする

```yml
  judgement:
    - name: same
      config:
        when_any:
          - req.path == '/test0'
          - req.path == '/test1'
```

[Template表記]: ../../template
[request]: ../../models/request
[response]: ../../models/response
