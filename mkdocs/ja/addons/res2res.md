res2res [:fa-github:][s1]
=========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res

APIレスポンスを形式を変えずに変換します。


[:fa-github:][s2] json_sort
---------------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/res2res/json_sort.py

JSONレスポンスの並び順をソートします。

!!! warning "処理がスキップされるケース"

    `content-type` が `text/json` や `application/json` でない場合はレスポンスがJSONでないとみなされ処理がスキップされます。


### Config

#### Definitions

##### Root

|       Key        |        Type         |                    Description                     | Example | Default |
| ---------------- | ------------------- | -------------------------------------------------- | ------- | ------- |
| items            | [Sorter[]](#sorter) | ソート設定のリスト                                 |         |         |
| default_encoding | (string)            | レスポンスヘッダに指定がない場合のエンコーディング | euc-jp  | urf8    |

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

[request-condition]: /ja/models/request-condition
