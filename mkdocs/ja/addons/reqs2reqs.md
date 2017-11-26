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
