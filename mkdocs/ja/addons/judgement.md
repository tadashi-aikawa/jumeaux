judgement [:fa-github:][s1]
===========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement

プロパティ差分情報を元に ステータス(Same/Different)を決定します。


[:fa-github:][s2] ignore_properties
-----------------------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/judgement/ignore_properties.py

以下2つの情報を生成します。

* configで指定したプロパティを無視した上で判定したステータス
* 無視したプロパティのキー と 無視するために参照した設定
    * Reportの`ignores`に出力されます

!!! warning

    既に同レイヤーのアドオンでSameと判定されている場合、本アドオンは実行されません。
    今のところ他のアドオンはありませんが...


### Config

#### Definitions

##### Root

|   Key   |        Type         | Description | Example | Default |
| ------- | ------------------- | ----------- | ------- | ------- |
| ignores | [Ignore[]](#ignore) | 無視設定    |         |         |

##### Ignore

|    Key     |           Type            |           Description           |        Example         | Default |
| ---------- | ------------------------- | ------------------------------- | ---------------------- | ------- |
| title      | (string)                  | タイトル                        | IDは毎回変わるので無視 |         |
| conditions | [Condition[]](#condition) | 本設定を反映させるRequestの条件 |                        |         |
| image      | (string)                  | 画像のURL                       | https://hoge.png       |         |
| link       | (string)                  | 参考URL                         | https://reference.html |         |

!!! note "`image`と`link`について"

    画像のURLと参考URLはViewerなどで利用されることを想定しています。

##### Condition

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
