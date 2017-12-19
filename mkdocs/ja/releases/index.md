Releases
========

主なリリース情報を記載します。  
全ての変更はGitHubのコミットログをご覧ください。

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


[final/miroir]: /ja/addons/final#miroir
