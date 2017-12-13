RequestCondition
================

requestの絞込を設定するため必要なRequestConditionの定義です。

Definitions
-----------

### RequestCondition

|  Key   |           Type           |                     Description                      | Example | Default |
| ------ | ------------------------ | ---------------------------------------------------- | ------- | ------- |
| name   | [Matchers](#matchers)    | nameの検索条件                                       |         |         |
| path   | [Matchers](#matchers)    | pathの検索条件                                       |         |         |
| and_or | (AndOr) :fa-info-circle: | `name`と`path`の組み合わせをAND/ORどちらで判定するか |         | and     |

??? info "AndOr"

    --8<--
    ja/constants/and_or.md
    --8<--

### Matchers

|   Key    |           Type           |            Description             | Example | Default |
| -------- | ------------------------ | ---------------------------------- | ------- | ------- |
| items    | [Matcher[]](#matcher)    | マッチング条件のリスト             |         |         |
| and_or   | (AndOr) :fa-info-circle: | `items` をAND/ORどちらで判定するか |         | and     |
| negative | (bool)                   | 否定条件とするか                   | true    | false   |

??? info "AndOr"

    --8<--
    ja/constants/and_or.md
    --8<--

### Matcher

|   Key    |  Type  |    Description     |     Example     | Default |
| -------- | ------ | ------------------ | --------------- | ------- |
| regexp   | string | 完全一致の正規表現 | `same\d{0-2}.*` |         |
| negative | (bool) | 否定条件とするか   | true            | false   |


Examples
--------

### `path`が`/traffic`と一致するもの

```yml
path:
  items:
    - regexp: /traffic
```

### 複雑な条件

以下のいずれかを満たすもの

* `name`にignoreを含まない もしくは `name`がignoreを含んでもjumeauxから始まるもの
* `path`にjumeauxを含み、ignoreを含まないもの

```yml
name:
  items:
    - regexp: .*ignore.*
      negative: true
    - regexp: jumeaux.+
  and_or: or
path:
  items:
    - regexp: .*jumeaux.*
    - regexp: .*ignore.*
      negative: true
and_or: or
```
