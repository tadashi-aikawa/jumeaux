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

```yml
reqs2reqs:
  - name: head
    config:
      size: 10
```


[:fa-github:][filter] filter
----------------------------

[filter]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/filter.py

!!! todo

    Comming soon...


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

[request]: /models/request

##### Location

| Name | Description |
| ---- | ----------- |
| head | 先頭        |
| tail | 末尾        |


#### Examples

##### 末尾に`/rest/sample?word=hoge`というリクエストを追加する

```yml
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

!!! todo

    Comming soon...


[:fa-github:][shuffle] shuffle
------------------------------

[shuffle]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/reqs2reqs/shuffle.py

!!! todo

    Comming soon...


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

```yml
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
| message  | string | 送信するメッセージ :fa-info-circle:      | <pre>{title}を中断しました</pre> |         |

!!! todo "notifierについて"

    TODO: 後日マニュアルに記載します。
    それまでの間、設定例はテストコード[test_empty_guard]を参考にしてください。


!!! info "送信するメッセージについて"

    [Report](../getstarted/configuration.md)で定義されたプロパティを使用する事ができます。

[test_empty_guard]: https://github.com/tadashi-aikawa/jumeaux/tree/master/tests/addons/reqs2reqs/test_empty_guard.py

#### Examples

##### リクエストが空の場合に処理を中断する

```yml
reqs2reqs:
  - name: empty_guard
```

##### リクエストが空の場合にnotifier jumeauxを使用して通知 および 処理の中断をする

```yml
reqs2reqs:
  - name: empty_guard
    config:
      notifies:
        - notifier: jumeaux
          message: "{title} notify!"
```

!!! hint "`notifier: jumeaux`について"

    Jumeauxのconfigに以下のような設定が必要です。

    ```yml
    notifiers:
      jumeaux:
        type: slack
        channel: "#jumeaux"
        username: jumeaux
        icon_emoji: "jumeaux"
    ```
