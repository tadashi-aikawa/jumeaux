did_challenge [:fa-github:][s1]
===============================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/did_challenge

次のchallengeに移る前に処理をします。


[:fa-github:][sleep] sleep
--------------------------

[sleep]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/did_challenge/sleep.py

指定した時間、待機します。


### Config

#### Definitions

| Key | Type  |            Description             | Example | Default |
| --- | ----- | ---------------------------------- | ------- | ------- |
| min | float | 待機時間 :fa-info-circle: の下限値 | 0.1     |         |
| max | float | 待機時間 :fa-info-circle: の上限値 | 1.0     |         |

!!! info "待機時間について"

    待機時間は`min`から`max`の範囲でランダムに決定されます。
    固定値にしたい場合は`min`と`max`に指定したい値を設定してください。

#### Examples

##### ランダムで0.1～1.0秒待機する

```yml
did_challenge:
  - name: sleep
    config:
      min: 0.1
      max: 1.0
```

##### 0.5秒待機する

```yml
did_challenge:
  - name: sleep
    config:
      min: 0.5
      max: 0.5
```


[:fa-github:][tag] tag
----------------------

[tag]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/did_challenge/tag.py

リクエスト結果ごとにタグを設定します。


### Config

#### Definitions

##### Root

| Key        | Type                      | Description    | Example | Default |
|------------|---------------------------|----------------|---------|---------|
| conditions | [Condition[]](#condition) | タグの値と条件 |         |         |

##### Condition

| Key  | Type | Description                                   | Example                     | Default |
|------|------|-----------------------------------------------|-----------------------------|---------|
| tag  | str  | 付与するタグ :fa-info-circle:                 | `{one[type]}`               |         |
| when | str  | [jinja2の式]に準拠した条件式 :fa-info-circle: | <pre>"name == 'hoge'"</pre> |         |

[jinja2の式]: http://jinja.pocoo.org/docs/2.10/templates/#expressions

!!! info "付与するタグについて"

    [Trial](../models/trial.md)プロパティを使用する事ができます。  
    要素へのアクセスは辞書アクセスです。

!!! info "whenで指定できるプロパティ"

    [Trial](../models/trial.md)プロパティを指定する事ができます。  
    要素へのアクセスはドットアクセスか辞書アクセスです。


#### Examples

##### Trialのnameが`json`のとき、`json`というタグを付ける

```yml
did_challenge:
  - name: tag
    config:
      conditions:
        - tag: json
          when: "name == 'json'"
```

##### それぞれのレスポンスタイプをタグとして付ける

```yml
did_challenge:
  - name: tag
    config:
      conditions:
        - tag: "tag:{one[type]}"
        - tag: "tag:{other[type]}"
```

