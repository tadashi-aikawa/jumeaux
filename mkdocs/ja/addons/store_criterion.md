store_criterion [:fa-github:][s1]
=================================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion

APIレスポンスを保存する基準を決定します。


[:fa-github:][general] general
------------------------------

[general]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion/general.py

レスポンスの保存基準を決める標準アドオンです。


### Config

#### Definitions

|   Key    |   Type                    |                       Description      |    Example    | Default |
| -------- | ------------------------- | -------------------------------------- |-------------- | ------- |
| statuses | Status[] :fa-info-circle: | レスポンスを保存するステータスのリスト | `[different]` |         |

??? info "Status"

    --8<--
    ja/constants/status.md
    --8<--

#### Examples

##### 差分のあるレスポンスだけを保存する

```yml
store_criterion:
  - name: general
    config:
      statuses:
        - different
```

##### 成功したリクエスト結果だけを保存する

```yml
store_criterion:
  - name: general
    config:
      statuses:
        - same
        - different
```



[:fa-github:][free] free
------------------------

[free]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion/free.py

細かな条件を指定してレスポンスの保存基準を決めることができます。


### Config

#### Definitions

| Key      | Type  | Description                                   | Example                      | Default |
|----------|-------|-----------------------------------------------|------------------------------|---------|
| when_any | str[] | [jinja2の式]に準拠した条件式 :fa-info-circle: | <pre>'"2" in req.path'</pre> |         |

[jinja2の式]: http://jinja.pocoo.org/docs/2.10/templates/#expressions

!!! info "when_anyで指定できるプロパティ"

    | key       | Type                    | Description           |
    |-----------|-------------------------|-----------------------|
    | status    | Status :fa-info-circle: | ステータス
    | req       | [Request][request]      | リクエスト情報        |
    | res_one   | [Response][response]    | oneのレスポンス情報   |
    | res_other | [Response][response]    | otherのレスポンス情報 |

    ??? info "Status"

        --8<--
        ja/constants/status.md
        --8<--


#### Examples

##### pathが`/test`またはステータスがSameの結果は保存する

```yml
store_criterion:
  - name: free
    config:
    when_any:
      - req.path == '/test'
      - status == 'same'
```

[request]: ../../models/request
[response]: ../../models/response

