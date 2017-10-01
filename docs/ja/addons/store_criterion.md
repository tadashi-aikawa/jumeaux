store_criterion [:fa-github:][s1]
=================================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion

APIレスポンスを保存する基準を決定します。


[:fa-github:][s2] general
-------------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/store_criterion/general.py

レスポンスの保存基準を決める標準アドオンです。


### Config

#### Definitions

|   Key    |   Type   |                       Description                       |    Example    | Default |
| -------- | -------- | ------------------------------------------------------- | ------------- | ------- |
| statuses | Status[] | レスポンスを保存するステータスのリスト :fa-info-circle: | `[different]` |         |

??? info "Status"

    --8<--
    models/status.md
    --8<--

#### Examples

##### 差分のあるレスポンスだけを保存する

```yml
- name: jumeaux.addons.store_criterion.general
  config:
    statuses:
      - different
```

##### 成功したリクエスト結果だけを保存する

```yml
- name: jumeaux.addons.store_criterion.general
  config:
    statuses:
      - same
      - different
```
