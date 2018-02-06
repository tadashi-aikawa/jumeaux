Releases
========

主なリリース情報を記載します。  
全ての変更はGitHubのコミットログをご覧ください。


## :package: 0.38.0

:fa-calendar: `2018/02/06`

??? info "ログの出力設定インタフェースと出力内容を変更しました"

    実行時にvオプションを指定することで必要なレベルのログを出力することができます。

    * 指定無し: 差分のあったケースの出力など最低限必要なレベル
    * `-v`:     ケースの結果など途中経過を把握できるレベル
    * `-vv`:    問題が起きたときに利用者が調査依頼できるレベル
    * `-vvv`:   問題が起きたときに開発者がデバッグで利用するレベル

    !!! danger "`output.logger`は近い内に非サポートになります"


## :package: 0.37.0

:fa-calendar: `2018/01/26`

??? info "リクエストの接続失敗最大数を指定できるようにしました"
    
    * 対応前の接続失敗最大数は3
    * 引数の場合は `--max-retries` を指定します
    * 設定の詳細は [configuration] をご覧ください

!!! hint "SLACK_INCOMING_WEBHOOKS_URLが環境変数に設定されていないとき実行前にエラーで終了するようにしました ([final/slack])"

!!! hint "実行ログの出力を改善しました"


## :package: 0.36.2

:fa-calendar: `2018/01/17`

??? bug "バイナリなどencodingの推測が不可能な場合に強制終了する不具合を修正しました"

    * encodingの予測すら不可能な場合はUTF-8でdecodeします
    * decodeできない文字が出現した場合は文字化けとして扱います
    * バイナリをTextとして扱うアドオンなどを使用していなければdecodeはされません

??? hint "Jumeauxのバージョンを開始ログに追記しました"

    * 実行時の設定が出力される直前に表示されます
    * 動作確認や不具合問い合わせ時にご利用ください


## :package: 0.36.1

:fa-calendar: `2018/01/15`

??? bug "特定のケースで不適切なencodingによるdecode/encodeされていた不具合を修正しました"

    content-typeのcharsetが指定されていない場合にdefault-encodingを使用していましたが、以下の順で判断するよう変更しました。

    1. xmlなどbodyにエンコーディング情報が含まれる場合はそれを採用する
    2. 1が存在しない場合はbodyの内容からエンコーディングを推測する

    !!! danger "default_encodingについて"

        * 一部アドオンの設定に定義されている`default_encoding`は機能しなくなります
        * 次のマイナーバージョンアップで`default_encoding`を削除します


## :package: 0.36.0

:fa-calendar: `2018/01/11`

??? danger "`jumeaux run`コマンドのrunを省略できなくなりました"

    * runなしで実行している場合はrunを付けるようにしてください

!!! bug "jumeaux retryコマンドが実行できない不具合を修正しました"

??? hint "実行時の設定をログに出力するようにしました"

    * `config.yml`, `report.json`, コマンドライン引数の全てを考慮した値が出力されます
    * 動作確認や不具合問い合わせ時にご利用ください


## :package: 0.35.0

:fa-calendar: `2017/12/26`

??? danger "filterアドオンのconfig仕様に破壊的変更があります ([reqs2reqs/filter])"

    * 新しい仕様を [reqs2reqs/filter] でご確認の上、設定を移行してください

??? hint "アドオンのドキュメントが完成しました"

    * [addons] TODOのアドオンが無くなりました
    * 部分的にTODOの項目は今後対応していきます


## :package: 0.34.1

:fa-calendar: `2017/12/23`

??? bug "CLIの引数で指定した値が通知メッセージに反映されない不具合を修正しました ([reqs2reqs/empty_guard])"

    例: `notifies[].message`に`"{hoge} is End"`と設定し、jumeauxの実行引数に`--title TITLE`を指定した場合

    * 0.34.1未満 => `None is End`
    * 0.34.1     => `TITLE is End`


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


[configuration]: /ja/getstarted/configuration
[addons]: /ja/addons
[reqs2reqs/empty_guard]: /ja/addons/reqs2reqs#empty_guard
[reqs2reqs/filter]: /ja/addons/reqs2reqs#filter
[reqs2reqs/replace]: /ja/addons/reqs2reqs#replace
[res2dict/richplain]: /ja/addons/res2dict#block
[res2dict/block]: /ja/addons/res2dict#block
[final/miroir]: /ja/addons/final#miroir
[final/slack]: /ja/addons/final#slack
