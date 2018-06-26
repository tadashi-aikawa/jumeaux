Releases
========

主なリリース情報を記載します。  
全ての変更はGitHubのコミットログをご覧ください。

## :package: 0.55.0

:fa-calendar: `2018-06-26`

??? info "store_criterion/freeアドオンを追加しました ([store_criterion/free])"

    * 指定した条件のいずれかに一致する場合のみ結果をdumpさせることができます
    * 詳しくは[store_criterion/free]をご覧下さい

??? info "property解析用のdictをjsonファイルとしてdumpするようにしました"

    * JSON以外のデータ形式に対してプロパティベースで解析したい場合に利用できます
    * ファイルは`one`, `other`と同階層の`one-props`, `other-props`ディレクトリ配下に作成されます


## :package: 0.54.0

:fa-calendar: `2018-06-22`

??? info "judgement/sameアドオンを追加しました ([judgement/same])"

    * 指定した条件のいずれかに一致する場合、ステータスをSameにすることができます
        * 例: ファイルタイプがバイナリでサイズが変わらない場合はSameとする
    * 詳しくは[judgement/same]をご覧下さい

??? info "リクエストのURLエンコーディング候補を指定できるようにしました ([log2reqs/plain])"

    * `candidate_for_url_encodings`に指定した複数のエンコーディングを候補として判定します
    * 詳しくは[log2reqs/plain]をご覧下さい


## :package: 0.53.0

:fa-calendar: `2018-06-11`

??? info "whenオプションを追加しました ([res2res/json])"

    * jinja2の式を使って柔軟な条件を指定することができます
    * 詳しくは[res2res/json]をご覧下さい

??? info "キーのみが指定されたクエリを除外しないオプションを追加しました ([log2reqs/plain]) ([log2reqs/csv])"

    * `keep_blank: true`を指定すると`key=`や`key`を空値として解釈します
    * 詳しくは[log2reqs/plain]や[log2reqs/csv]をご覧下さい


## :package: 0.52.0

:fa-calendar: `2018-05-28`

??? info "テスト結果のtrialsにtypeプロパティを追加しました"

    * 該当レスポンスがどのようなファイルタイプであるかを示すパラメータです
    * レスポンスヘッダのcontent-typeから判断します
      * [RFC-2045](https://tools.ietf.org/html/rfc2045#section-5.1)のsubtypeで判断します
    * 一般的ではないtypeを変換するには[res2res/type]を使用して下さい

??? info "res2res/typeアドオンを追加しました ([res2res/type])"

    * 特定条件に一致する場合にtypeを変更することができます
    * 詳しくは[res2res/type]をご覧下さい

??? danger "以下アドオンのconfigから`mime_types`を削除しました"

    * [res2dict/json]
    * [res2dict/xml]
    * [res2dict/html]
    * [res2dict/block]
    * [dump/html]
    * [dump/xml]

    一般的ではないmime-typeが返却される場合は[res2res/type]を使用して下さい。


## :package: 0.51.0

:fa-calendar: `2018-05-13`

??? info "res2res/jsonアドオンを追加しました ([res2res/json])"

    * 任意のロジックを指定してレスポンスを強制的にjsonへ変換することができます
    * 詳しくは[res2res/json]をご覧下さい

!!! bug "jsonのトップレベルが配列の時に強制終了する不具合を修正しました ([res2dict/json])"


## :package: 0.50.0

:fa-calendar: `2018-05-10`

??? info "`jumeaux viewer`コマンドを追加しました"

    * Jumeauxを実行して結果が出力されたらViewerをlivereloadすることができます
    * 詳しくは[viewer]をご覧下さい

!!! info "Viewerで実行終了日時を表示するようにしました ([final/viewer])"


## :package: 0.49.0

:fa-calendar: `2018-05-06`

??? danger "デフォルトで標準出力に結果を出力しないようにしました"

    * 今までのようにjsonを出力するには[final/json]アドオンを使用してください

??? info "viewerアドオンを追加しました ([final/viewer])"

    * 結果をGUIで確認可能なHTMLファイルを出力します
    * [final/json]アドオンと一緒に使う必要があります
    * 詳しくは[final/viewer]をご覧下さい

    [![](https://dl.dropboxusercontent.com/s/btw02l0xsn10bzl/0.49.0-1.png)](https://dl.dropboxusercontent.com/s/btw02l0xsn10bzl/0.49.0-1.png)

??? info "jsonアドオンを追加しました ([final/json])"

    * 結果をjsonとして出力します
    * 詳しくは[final/json]をご覧下さい

??? info "summaryアドオンを追加しました ([final/summary])"

    * 結果を1画面に納まる程度のsummaryとして出力します
    * 詳しくは[final/summary]をご覧下さい

??? info "`jumeaux server`コマンドに`-v`オプションを追加しました"

    * `-v`オプションを指定する場合はリクエストヘッダを標準エラー出力に出力します (今までと同じ挙動)


## :package: 0.48.0

:fa-calendar: `2018-04-30`

??? info "htmlアドオンを追加しました ([res2dict/html])([dump/html])"

    * HTMLをプロパティとして解析したり、保存時にフォーマットすることができます
    * 詳しくは [res2dict/html] と [dump/html] をご覧下さい


## :package: 0.47.0

:fa-calendar: `2018-04-17`

??? info "renameアドオンを追加しました ([reqs2reqs/rename])"

    * 特定条件に一致するリクエストの名称を変更することができます
    * jinja2の式を使って柔軟な条件を指定することができます
    * 詳しくは [reqs2reqs/rename] をご覧下さい

??? info "User agentに適切な値を設定するようにしました"

    * 詳しくは[Issue #66](https://github.com/tadashi-aikawa/jumeaux/issues/66)をご覧下さい


## :package: 0.46.1

:fa-calendar: `2018-04-05`

!!! bug "レスポンスのエンコーディングが推測した結果でかつ不適切なとき強制終了する不具合を修正しました ([res2res/json_sort])"

??? danger "default_encodingを非推奨にしました ([res2res/json_sort])"

    * 近い内に削除します
    * 削除された後は指定するとエラーになりますので注意してください
    * [res2res/json_sort]の仕様からは既に削除済みです


## :package: 0.46.0

:fa-calendar: `2018-04-04`

??? danger "`jumeaux init`で作成できるテンプレートの候補と中身が変更されました"

    * 新しい候補を表示するには`jumeaux init help`を実行してください
    * 新しいテンプレートは`python -m http.server`を実行したときに動作する想定で作られています
    * 後のバージョンにてjumeauxコマンド経由で上記を実行/停止できるようにする予定です


## :package: 0.45.0

:fa-calendar: `2018-03-31`

!!! info "DynamoDBへ送信するデータにelapsed_sec(実行秒)を追加しました ([final/miroir])"


## :package: 0.44.0

:fa-calendar: `2018-03-30`

??? danger "reportに出力される日付フォーマットをISO 8601に変更しました"

    * `2000/01/01 10:00:00` => `2000-01-01T10:00:00.000000` のように変わります

!!! hint "デバッグログが出力されるようになりました ([res2dict])"


## :package: 0.43.1

:fa-calendar: `2018-03-29`

!!! note "内部的なリファクタリングとテストの整備をしました"


## :package: 0.43.0

:fa-calendar: `2018-03-26`

??? info "特定のタグを持つアドオンをスキップする実行オプションを追加しました"

    * `--skip-addon-tag`オプションでスキップ対象のタグを指定します
        * `--skip-addon-tag`は複数指定可能
    * アドオンにタグを設定するには [addons/addon] の定義をご覧ください


## :package: 0.42.0

:fa-calendar: `2018-03-02`

??? info "レスポンスの文字コードが不明なとき任意のエンコーディングを指定するオプションを追加しました"

    * OneとOtherそれぞれに対して1つずつ設定できます
    * 未指定の場合はレスポンスボディからエンコーディングを推測します
        * 推測の場合、パフォーマンスが著しく低下します
    * 設定の詳細は [configuration] から AccessPoint の`default_response_encoding`をご覧ください


## :package: 0.41.2

:fa-calendar: `2018-02-27`

??? hint " 文字化けしたレスポンスをdumpできるようにしました([dump/xml])([dump/json])"

    * 化けている文字は`?`に置換されます
    * 0.41.1までは強制終了していました


## :package: 0.41.1

:fa-calendar: `2018-02-16`

!!! note "requestsライブラリのwarningを消しました"


## :package: 0.41.0

:fa-calendar: `2018-02-15`

!!! bug "`jumeaux init`が動作しない不具合を修正しました"

??? hint "アドオンの引数にoneとotherのdictを追加しました ([judgement/ignore_properties])"

    * アドオン作成者以外は影響ありません
    * 詳細は [addons] の設計図をご覧ください


## :package: 0.40.0

:fa-calendar: `2018-02-13`

!!! info "`jumeaux init addon`でアドオンサンプルプロジェクトを作成できるようにしました"

    !!! warning "この機能はβ版です。予告なく削除される可能性があります"

!!! hint "`jumeaux init`で作成されたファイルをログ出力するようにしました"


## :package: 0.39.1

:fa-calendar: `2018-02-12`

!!! bug "`jumeaux init`が動作しない不具合修正"


## :package: 0.39.0

:fa-calendar: `2018-02-12`

!!! note "内部的な設定ファイルの整備を行いました"


## :package: 0.38.1

:fa-calendar: `2018-02-09`

!!! bug "Dockerfileで作成したイメージが起動しない不具合修正"


## :package: 0.38.0

:fa-calendar: `2018-02-06`

??? info "ログの出力設定インタフェースと出力内容を変更しました"

    実行時にvオプションを指定することで必要なレベルのログを出力することができます。

    * 指定無し: 差分のあったケースの出力など最低限必要なレベル
    * `-v`:     ケースの結果など途中経過を把握できるレベル
    * `-vv`:    問題が起きたときに利用者が調査依頼できるレベル
    * `-vvv`:   問題が起きたときに開発者がデバッグで利用するレベル

    !!! danger "`output.logger`は近い内に非サポートになります"


## :package: 0.37.0

:fa-calendar: `2018-01-26`

??? info "リクエストの接続失敗最大数を指定できるようにしました"
    
    * 対応前の接続失敗最大数は3
    * 引数の場合は `--max-retries` を指定します
    * 設定の詳細は [configuration] をご覧ください

!!! hint "SLACK_INCOMING_WEBHOOKS_URLが環境変数に設定されていないとき実行前にエラーで終了するようにしました ([final/slack])"

!!! hint "実行ログの出力を改善しました"


## :package: 0.36.2

:fa-calendar: `2018-01-17`

??? bug "バイナリなどencodingの推測が不可能な場合に強制終了する不具合を修正しました"

    * encodingの予測すら不可能な場合はUTF-8でdecodeします
    * decodeできない文字が出現した場合は文字化けとして扱います
    * バイナリをTextとして扱うアドオンなどを使用していなければdecodeはされません

??? hint "Jumeauxのバージョンを開始ログに追記しました"

    * 実行時の設定が出力される直前に表示されます
    * 動作確認や不具合問い合わせ時にご利用ください


## :package: 0.36.1

:fa-calendar: `2018-01-15`

??? bug "特定のケースで不適切なencodingによるdecode/encodeされていた不具合を修正しました"

    content-typeのcharsetが指定されていない場合にdefault-encodingを使用していましたが、以下の順で判断するよう変更しました。

    1. xmlなどbodyにエンコーディング情報が含まれる場合はそれを採用する
    2. 1が存在しない場合はbodyの内容からエンコーディングを推測する

    !!! danger "default_encodingについて"

        * 一部アドオンの設定に定義されている`default_encoding`は機能しなくなります
        * 次のマイナーバージョンアップで`default_encoding`を削除します


## :package: 0.36.0

:fa-calendar: `2018-01-11`

??? danger "`jumeaux run`コマンドのrunを省略できなくなりました"

    * runなしで実行している場合はrunを付けるようにしてください

!!! bug "jumeaux retryコマンドが実行できない不具合を修正しました"

??? hint "実行時の設定をログに出力するようにしました"

    * `config.yml`, `report.json`, コマンドライン引数の全てを考慮した値が出力されます
    * 動作確認や不具合問い合わせ時にご利用ください


## :package: 0.35.0

:fa-calendar: `2017-12-26`

??? danger "filterアドオンのconfig仕様に破壊的変更があります ([reqs2reqs/filter])"

    * 新しい仕様を [reqs2reqs/filter] でご確認の上、設定を移行してください

??? hint "アドオンのドキュメントが完成しました"

    * [addons] TODOのアドオンが無くなりました
    * 部分的にTODOの項目は今後対応していきます


## :package: 0.34.1

:fa-calendar: `2017-12-23`

??? bug "CLIの引数で指定した値が通知メッセージに反映されない不具合を修正しました ([reqs2reqs/empty_guard])"

    例: `notifies[].message`に`"{hoge} is End"`と設定し、jumeauxの実行引数に`--title TITLE`を指定した場合

    * 0.34.1未満 => `None is End`
    * 0.34.1     => `TITLE is End`


## :package: 0.34.0

:fa-calendar: `2017-12-22`

??? info "empty_guardアドオンを追加しました ([reqs2reqs/empty_guard])"

    * `reqs2reqs`のレイヤーでリクエストを確認し、0件の場合は処理を中断させることができます
    * 中断した場合は任意の方法で通知することができます (今はSlackのみ)
    * 詳細は [reqs2reqs/empty_guard] をご覧ください
    * ステータスコードは1を返却します。正常終了にしたいケースもあると思いますのでオプション追加で検討しています


## :package: 0.33.0

:fa-calendar: `2017-12-20`

??? danger "richplainアドオンの名称をblockアドオンに変更し、機能を追加しました ([res2dict/block])"

    * 空行区切りのテキストをブロックとして扱い、任意のパターンで変換することができます
    * 詳細は [res2dict/block] をご覧ください


## :package: 0.32.0

:fa-calendar: `2017-12-19`

??? info "richplainアドオンを追加しました ([res2dict/richplain])"
    
    Version 0.33.0で名称が変更されています

    * 特殊な形式で記載されたテキストをdictに変換することができます
    * 詳細は [res2dict/block] をご覧ください


## :package: 0.31.1

:fa-calendar: `2017-12-19`

??? hint "レスポンスヘッダにエンコーディング情報が無い場合、UTF8ではなく推測したエンコーディングでデコードするようにしました"
    
    APIにリクエストした結果(body)をUnicodeへデコードする場合の話です


## :package: 0.31.0

:fa-calendar: `2017-12-14`

??? hint "リクエスト結果が返却された後の処理を高速化しました"
    
    レスポンスサイズが大きく、結果がほぼSameの場合は10倍以上速くなるケースもあります


## :package: 0.30.1

:fa-calendar: `2017-12-06`

!!! hint "when_notプロパティをwhenに変更しました ([final/miroir])"


[configuration]: /ja/getstarted/configuration
[viewer]: /ja/getstarted/quickstart/#viewer
[addons]: /ja/addons
[addons/addon]: /ja/addons#addon
[log2reqs/plain]: /ja/addons/log2reqs#plain
[log2reqs/csv]: /ja/addons/log2reqs#csv
[reqs2reqs/empty_guard]: /ja/addons/reqs2reqs#empty_guard
[reqs2reqs/filter]: /ja/addons/reqs2reqs#filter
[reqs2reqs/replace]: /ja/addons/reqs2reqs#replace
[reqs2reqs/rename]: /ja/addons/reqs2reqs#rename
[res2res/json]: /ja/addons/res2res#json
[res2res/json_sort]: /ja/addons/res2res#json_sort
[res2res/type]: /ja/addons/res2res#type
[res2dict]: /ja/addons/res2dict
[res2dict/json]: /ja/addons/res2dict#json
[res2dict/html]: /ja/addons/res2dict#html
[res2dict/xml]: /ja/addons/res2dict#xml
[res2dict/block]: /ja/addons/res2dict#block
[judgement/ignore_properties]: /ja/addons/judgement#ignore_properties
[judgement/same]: /ja/addons/judgement#same
[store_criterion/free]: /ja/addons/store_criterion#free
[dump/xml]: /ja/addons/dump#xml
[dump/html]: /ja/addons/dump#html
[dump/json]: /ja/addons/dump#json
[final/miroir]: /ja/addons/final#miroir
[final/slack]: /ja/addons/final#slack
[final/json]: /ja/addons/final#json
[final/summary]: /ja/addons/final#summary
[final/viewer]: /ja/addons/final#viewer
