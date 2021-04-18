Addons
======

Jumeauxではアドオンを利用して処理をカスタマイズすることができます。  
アドオンは自作することも可能です。


System structure
----------------

以下はJumeauxの処理を図で表したものです。  
画像の青色の部分がアドオンレイヤーです。

[![](https://cacoo.com/diagrams/9606d6pSveEhBPoH-89A6C.png)](https://cacoo.com/diagrams/9606d6pSveEhBPoH#89A6C)


Add-on specifications
---------------------

各アドオンレイヤーに属するアドオンの仕様は以下のページに記載しています。

| アドオンレイヤー  | アドオンレイヤーの概要                          |
|-------------------|-------------------------------------------------|
| [log2reqs]        | 任意のFormatをリクエスト形式に変換する          |
| [reqs2reqs]       | リクエスト形式を同し形式の別の値に変換する      |
| [res2res]         | APIレスポンスを判定前に変換する                 |
| [res2dict]        | APIレスポンスを差分比較で利用するdictに変換する |
| [judgement]       | dict同士を比較して判定ステータスを決定する      |
| [store_criterion] | APIレスポンスを保存する基準を決定する           |
| [dump]            | APIレスポンスを保存前に加工する                 |
| [did_challenge]   | 次のchallengeに移る前に処理をする               |
| [final]           | jumeauxの処理が完了する前に処理をする           |

[log2reqs]: log2reqs
[reqs2reqs]: reqs2reqs
[res2res]: res2res
[res2dict]: res2dict
[judgement]: judgement
[store_criterion]: store_criterion
[dump]: dump
[did_challenge]: did_challenge
[final]: final


Configuration Definitions
-------------------------

アドオンを使用する場合は以下の定義に従って、[設定ファイル](ja/getstarted/configuration)に追加してください。

### Addons

| Key             | Type                | Description                 | Example | Default |
|-----------------|---------------------|-----------------------------|---------|---------|
| log2reqs        | [Addon](#addon)     | [log2reqs]のアドオン        |         |         |
| reqs2reqs       | ([Addon[]](#addon)) | [reqs2reqs]のアドオン       |         |         |
| res2res         | ([Addon[]](#addon)) | [res2res]のアドオン         |         |         |
| res2dict        | ([Addon[]](#addon)) | [res2dict]のアドオン        |         |         |
| judgement       | ([Addon[]](#addon)) | [judgement]のアドオン       |         |         |
| store_criterion | ([Addon[]](#addon)) | [store_criterion]のアドオン |         |         |
| dump            | ([Addon[]](#addon)) | [dump]のアドオン            |         |         |
| did_challenge   | ([Addon[]](#addon)) | [did_challenge]のアドオン   |         |         |
| final           | ([Addon[]](#addon)) | [final]のアドオン           |         |         |



### Addon

アドオン単位での設定です。

| Key      | Type       | Description                | Example      | Default  |
|----------|------------|----------------------------|--------------|----------|
| name     | string     | アドオン名称               | csv          |          |
| cls_name | (string)   | 実行するクラス名           | YourExecutor | Executor |
| config   | (Config)   | アドオンの設定             |              |          |
| include  | (string)   | 読み込む設定ファイルのパス |              |          |
| tags     | (string[]) | タグ                       |              |          |


Configuration Examples
----------------------

以下は設定の一例です。

```yaml
addons:
  log2reqs:
    name: csv

  reqs2reqs:
    - name: shuffle
    - name: head
      config:
        size: 10

  final:
    - name: slack
      tags:
        - production
      config:
        conditions:
          - payload:
              message_format: Finish Jumeaux!!
              channel: "#jumeaux"
              icon_emoji: ":innocent:"
```

この設定は以下のように動作します。

1. リクエストファイルをcsvと解釈してパースする
2. 1でパースした結果をシャッフルする
3. 2の結果 先頭10リクエストのみをテストする
4. `--skip-addon-tag production`が指定されていなければ最後にSlackで通知する

4つのアドオンが使用されており、仕様とconfigの定義は各アドオンページをご覧下さい。

* [log2reqs/csv]
* [reqs2reqs/shuffle]
* [reqs2reqs/head]
* [final/slack]

[log2reqs/csv]: log2reqs#csv
[reqs2reqs/shuffle]: reqs2reqs#shuffle
[reqs2reqs/head]: reqs2reqs#head
[final/slack]: final#slack

