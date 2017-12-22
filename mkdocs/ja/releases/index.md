Releases
========

主なリリース情報を記載します。  
全ての変更はGitHubのコミットログをご覧ください。


## :package: 0.34.0

:fa-calendar: `2017/12/22`

??? info "empty_guardアドオンを追加しました ([reqs2reqs/empty_guard])"

    * `reqs2reqs`のレイヤーでリクエストを確認し、0件の場合は処理を中断させることができます
    * 中断した場合は任意の方法で通知することができます (今はSlackのみ)
    * 詳細は [reqs2reqs/empty_guard] をご覧ください
    * ステータスコードは1を返却します。正常終了にしたいケースもあると思いますのでオプション追加で検討しています


## :package: 0.33.0

:fa-calendar: `2017/12/20`

??? danger "richplainアドオンの名称をblockアドオンに変更し、機能を追加しました ([res2dict/block])"

    * 空行区切りのテキストをブロックとして扱い、任意のパターンで変換することができます
    * 詳細は [res2dict/block] をご覧ください


## :package: 0.32.0

:fa-calendar: `2017/12/19`

??? info "richplainアドオンを追加しました ([res2dict/richplain])"
    
    * 特殊な形式で記載されたテキストをdictに変換することができます
    * 詳細は [res2dict/richplain] をご覧ください


## :package: 0.31.1

:fa-calendar: `2017/12/19`

??? hint "レスポンスヘッダにエンコーディング情報が無い場合、UTF8ではなく推測したエンコーディングでデコードするようにしました"
    
    APIにリクエストした結果(body)をUnicodeへデコードする場合の話です


## :package: 0.31.0

:fa-calendar: `2017/12/14`

??? hint "リクエスト結果が返却された後の処理を高速化しました"
    
    レスポンスサイズが大きく、結果がほぼSameの場合は10倍以上速くなるケースもあります


## :package: 0.30.1

:fa-calendar: `2017/12/06`

!!! hint "when_notプロパティをwhenに変更しました ([final/miroir])"


[reqs2reqs/empty_guard]: /ja/addons/reqs2reqs#empty_guard
[res2dict/richplain]: /ja/addons/res2dict#block
[res2dict/block]: /ja/addons/res2dict#block
[final/miroir]: /ja/addons/final#miroir
