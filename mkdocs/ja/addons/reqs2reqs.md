reqs2reqs [:fa-github:][s1]
===========================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs

リクエストを変換します。


[:fa-github:][head] head
------------------------

[head]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/head.py

リクエストの先頭部分を抽出します。

### Config

#### Definitions

| Key  | Type |      Description       | Example | Default |
| ---- | ---- | ---------------------- | ------- | ------- |
| size | int  | 抽出するリクエストの数 | 10      |         |


#### Examples

##### 先頭の10リクエストを抽出する

```yaml
  reqs2reqs:
    - name: head
      config:
        size: 10
```


[:fa-github:][filter] filter
----------------------------

[filter]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/filter.py

条件に一致するリクエストのみを抽出します。

### Config

#### Definitions

##### Root

| Key  | Type |       Description       |          Example          | Default |
| ---- | ---- | ----------------------- | ------------------------- | ------- |
| when | str  | 条件式 :fa-info-circle: | <pre>"qs.id.0 == 1"</pre> |         |


??? info "when"

    [jinja2の表現](http://jinja.pocoo.org/docs/2.10/templates)を利用できます。  
    プロパティは[request]で定義されたものを使用できます。


#### Examples

##### pathに`ok`が含まれ かつ nameに`OK`が含まれるリクエストのみ抽出する

```yaml
  res2res:
    - name: filter
      config:
        when: ('ok' in path) and ('OK' in name)
```


[:fa-github:][add] add
----------------------

[add]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/add.py

先頭または末尾にリクエストを追加します。

### Config

#### Definitions

##### root

|   Key    |          Type           |           Description           | Example | Default |
| -------- | ----------------------- | ------------------------------- | ------- | ------- |
| reqs     | [Request[]][request]    | 本設定を反映させるRequestの条件 |         |         |
| location | ([Location](#location)) | 先頭と末尾どちらに追加するか    | tail    | head    |


##### Location

| Name | Description |
| ---- | ----------- |
| head | 先頭        |
| tail | 末尾        |


#### Examples

##### 末尾に`/rest/sample?word=hoge`というリクエストを追加する

```yaml
  reqs2reqs:
    - name: add
      config:
        reqs:
          - path: /rest/sample
            qs: {word: [hoge]}
        location: tail
```


[:fa-github:][replace] replace
------------------------------

[replace]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/replace.py

条件に一致するリクエストを置換します。

### Config

#### Definitions

##### Root

|  Key  |          Type           |   Description    | Example | Default |
| ----- | ----------------------- | ---------------- | ------- | ------- |
| items | [Replacer[]](#replacer) | 置換設定のリスト |         |         |

##### Replacer

|   Key   |     Type     |       Description       |                 Example                 | Default |
| ------- | ------------ | ----------------------- | --------------------------------------- | ------- |
| when    | (str)        | 条件式 :fa-info-circle: | <pre>"qs.id.0 == 1"</pre>               |         |
| queries | dict[str[]]) | 置換するクエリ          | <pre>{"a": [1], "b": [2, 3]}</pre>      |         |
| headers | dict[str]    | 置換するヘッダ          | <pre>{"header1": 1, "header2": 2}</pre> |         |

??? info "when"

    [jinja2の表現](http://jinja.pocoo.org/docs/2.10/templates)を利用できます。  
    プロパティは[request]で定義されたものを使用できます。

!!! info "`queries`と`headers`について"

    リクエストに存在しないクエリやヘッダの場合は、設定した値が追加されます

#### Examples

##### pathが`/target`と一致するリクエストのクエリを置換する (`id=dummay_id`, `time=dummy_date`)

```yaml
  reqs2reqs:
    - name: replace
      config:
        items:
          - when: "path == /target"
            queries:
              id: ["dummy_id"]
              time: ["dummy_date"]
```


[:fa-github:][shuffle] shuffle
------------------------------

[shuffle]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/shuffle.py

リクエストの順序をシャッフルします。

### Config

#### Definitions

Config設定はありません。

#### Examples

##### リクエストをシャッフルする

```yaml
  reqs2reqs:
    - name: shuffle
```


[:fa-github:][repeat] repeat
----------------------------

[repeat]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/repeat.py

リクエスト全体を指定回数だけ複製します。

### Config

#### Definitions

|  Key  | Type | Description | Example | Default |
| ----- | ---- | ----------- | ------- | ------- |
| times | int  | 複製する数  | 10      |         |


#### Examples

##### リクエスト全体を10回複製する

```yaml
  reqs2reqs:
    - name: repeat
      config:
        times: 10
```


[:fa-github:][empty_guard] empty_guard
--------------------------------------

[empty_guard]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/empty_guard.py

リクエストが空の場合に処理を中断します。


### Prerequirements

--8<-- "ja/notify-prerequirements.md"


### Config

#### Definitions

##### root

|   Key    |         Type          |        Description         | Example | Default |
| -------- | --------------------- | -------------------------- | ------- | ------- |
| notifies | ([Notify[]](#notify)) | 処理を中断する時の通知設定 |         |         |

##### Notify

|   Key    |  Type  |               Description                |             Example              | Default |
| -------- | ------ | ---------------------------------------- | -------------------------------- | ------- |
| notifier | string | 使用する通知設定の名前  :fa-info-circle: | jumeaux                          |         |
| message  | string | 送信するメッセージ :fa-info-circle:      | <pre>{{ title }}を中断しました</pre> |         |


!!! info "notifierについて"

    通知設定の例は [config/examples] を参考にしてください。定義は [notifier] の通りです。

!!! info "messageついて"

    [Template表記]に対応しています。
    プロパティは[Configuration](../getstarted/configuration.md)で定義されたものを使用できます。


#### Examples

##### リクエストが空の場合に処理を中断する

```yaml
  reqs2reqs:
    - name: empty_guard
```

##### リクエストが空の場合にnotifier jumeauxを使用して通知 および 処理の中断をする

```yaml
  reqs2reqs:
    - name: empty_guard
      config:
        notifies:
          - notifier: jumeaux
            message: "{{ title }} notify!"
```

!!! hint "`notifier: jumeaux`について"

    Jumeauxのconfigに以下のような設定が必要です。

    ```yaml
    notifiers:
      jumeaux:
        type: slack
        channel: "#jumeaux"
        username: jumeaux
        icon_emoji: "jumeaux"
    ```


[request-condition]: ../../models/request-condition


[:fa-github:][rename] rename
----------------------------

[rename]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/rename.py

条件に一致するリクエストの名称を変更します。

### Config

#### Definitions

##### Root

| Key        | Type                      | Description  | Example | Default |
|------------|---------------------------|--------------|---------|---------|
| conditions | [Condition[]](#condition) | 変更値と条件 |         |         |

##### Condition

| Key  | Type |          Description          |              Example               | Default |
| ---- | ---- | ----------------------------- | ---------------------------------- | ------- |
| name | str  | 変更後の名称 :fa-info-circle: | <pre>{{ name }} ({{ path }})</pre> |         |
| when | str  | 条件式 :fa-info-circle:       | <pre>"qs.id.0 == 1"</pre>          |         |

!!! info "nameおよびwhenについて"

    [jinja2の表現](http://jinja.pocoo.org/docs/2.10/templates)を利用できます。  
    プロパティは[request]で定義されたものを使用できます。

    **nameはテンプレート部分を`{{ }}`で囲む必要があります。**  
    一方、**whenは式であるため`{{ }}`で囲む必要はありませんが、代わりに文字列はクォートで囲って下さい。**


#### Examples

##### pathに`target`という文字列が含まれる場合に`renamed`へ名称を変更する

```yaml
  reqs2reqs:
    - name: rename
      config:
        conditions:
          - name: renamed
            when: "'target' in path"
```

##### 複雑な条件

1. pathが小文字のアルファベット3文字である場合は`GOOD`へ名称を変更する
2. 1に該当せず`id`が1つだけ指定されており、かつ2より大きい場合は`<クエリのid>: <元の名称>`へ名称を変更する
  2-1. 例えば`id=4`で名称が`hoge`のとき、新しい名称は`4: hoge`となる
3. 1と2に該当しない場合は名称を変更しない

```yaml
  reqs2reqs:
    - name: rename
      config:
        conditions:
          - name: "GOOD"
            when: "path|reg('[a-z]{3}')"
          - name: "{{ qs.id.0 }}: {{ name }}"
            when: "qs.id|length == 1 and qs.id.0|int > 2"
```

[Template表記]: ../../template
[request]: ../../models/request
[notifier]: ../../models/notifier
[config/examples]: ../../getstarted/configuration/#examples

