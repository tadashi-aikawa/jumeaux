Addons
======

!!! warning

    Sorry, Now this page supports for Japanese only. (TODO: English)

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

| アドオンレイヤー  |             アドオンレイヤーの概要              |
| ----------------- | ----------------------------------------------- |
| [log2reqs]        | 任意のFormatをリクエスト形式に変換する          |
| [reqs2reqs]       | リクエスト形式を同し形式の別の値に変換する      |
| [res2res]         | APIレスポンスを形式を変えずに変換する           |
| [res2dict]        | APIレスポンスを差分比較で利用するdictに変換する |
| [judgement]       | dict同士を比較して判定ステータスを決定する      |
| [store_criterion] | APIレスポンスを保存する基準を決定する           |
| [dump]            | APIレスポンスを保存前に加工する                 |
| [did_challenge]   | 次のchallengeに移る前に処理をする               |
| [final]           | jumeauxの処理が完了する前に処理をする           |


[log2reqs]: /ja/addons/log2reqs
[res2res]: /ja/addons/res2res
[reqs2reqs]: /ja/addons/reqs2reqs
[res2dict]: /ja/addons/res2dict
[judgement]: /ja/addons/judgement
[store_criterion]: /ja/addons/store_criterion
[dump]: /ja/addons/dump
[did_challenge]: /ja/addons/did_challenge
[final]: /ja/addons/final
