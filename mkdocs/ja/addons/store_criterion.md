store_criterion [:fa-github:][s1]
=================================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion

APIレスポンスを保存する基準を決定します。


[:fa-github:][free] free
------------------------

[free]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion/free.py

細かな条件を指定してレスポンスの保存基準を決めることができます。


### Config

#### Definitions

| Key      | Type  | Description             | Example                      | Default |
|----------|-------|-------------------------|------------------------------|---------|
| when_any | str[] | 条件式 :fa-info-circle: | <pre>'"2" in req.path'</pre> |         |

!!! info "when_anyで指定できるプロパティ"

    [Template表記]に対応しています。
    プロパティは以下を使用できます。

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

```yaml
  store_criterion:
    - name: free
      config:
        when_any:
          - req.path == '/test'
          - status == 'same'
```

[Template表記]: ../../template
[request]: ../../models/request
[response]: ../../models/response

