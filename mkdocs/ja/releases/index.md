Releases
========

主なリリース情報を記載します。  
全ての変更はGitHubのコミットログをご覧ください。


## :package: 0.64.0

:fa-calendar: `2019-02-21`

??? info "ignoreアドオンを追加しました ([judgement/ignore])"

    * [judgement/ignore_properties]との差分は以下です
        * pathやqueryなどの条件絞り込みにjinja2フォーマットが使える
        * oneとotherのプロパティを式で比較して無視するかどうかを判定できる
        * 詳細は [judgement/ignore] をご覧下さい
    * [judgement/ignore_properties]を使っている場合はこちらへの移行をお願いします

??? fire "ignore_propertiesアドオンを非推奨にしました ([judgement/ignore_properties])"

    * Version 1.0 までの間に削除します
    * [judgement/ignore]アドオンへの移行をお願いします

??? fire "Reportのスキームを一部変更しました"

    * `ignores`を削除しました
    * [models/trial]の`diff_keys`を削除しました
    * [models/trial]の`diffs_by_cognition`を追加しました


## :package: 0.63.0

:fa-calendar: `2019-02-05`

??? info "whenやtagでレスポンスプロパティを利用できるようにしました([did_challenge/tag])"

    * OneとOtherそれぞれのレスポンスプロパティを参照できます
    * 詳細は [did_challenge/tag] をご覧下さい

??? info "Template functionにcalc_distance_kmを追加しました"

    * 座標間の概算距離を計算できます
    * 詳細は [template/#functions] をご覧下さい

??? hint "アドオンのExamplesに表記された設定例のインデントを調整しました"

    * コピーボタンでコピーした設定をそのまま貼り付けられるようになりました
    * もうペーストした後にインデント調整をする必要はありません :smile:

    [![](https://dl.dropboxusercontent.com/s/f9zsr96v994dh02/0.63.0-1.png)](https://dl.dropboxusercontent.com/s/f9zsr96v994dh02/0.63.0-1.png)


## :package: 0.62.0

:fa-calendar: `2019-01-24`

??? hint "whenやmessage_formatの値に構文エラーがある場合、実行直後にエラーを表示するようにしました"

    * jinja2フォーマットを使っている以下のアドオンが対象です
        * [reqs2reqs/empty_guard]
        * [reqs2reqs/rename]
        * [did_challenge/tag]
        * [final/slack]


## :package: 0.61.1

:fa-calendar: `2019-01-16`

!!! note "アドオンサンプルプロジェクトの依存関係が不適切だったのを修正しました"


## :package: 0.61.0

:fa-calendar: `2019-01-13`

??? info "アクセス先ごとにパスを制御できるようにしました"

    * OneとOtherそれぞれに対して、正規表現を含めたpathの置換ができます
    * 設定の詳細は [configuration] から AccessPoint の`path`をご覧ください


## :package: 0.60.0

:fa-calendar: `2018-12-12`

??? danger "formatを指定できる設定箇所の仕様をwhen(jinja2)の仕様にあわせました"

    以下のアドオンに影響があります。

    * [reqs2reqs/rename](https://tadashi-aikawa.github.io/jumeaux/ja/addons/reqs2reqs/#condition)
    * [reqs2reqs/empty_guard](https://tadashi-aikawa.github.io/jumeaux/ja/addons/reqs2reqs/#notify)
    * [did_challenge/tag](https://tadashi-aikawa.github.io/jumeaux/ja/addons/did_challenge/#condition)
    * [final/slack](https://tadashi-aikawa.github.io/jumeaux/ja/addons/final/#payload)

    代表的な変更点は以下3点です。

    * 変数表記は`{var}`ではなく`{{ var }}`で表現する
    * プロパティアクセスは全てドットアクセス(`obj.prop`)で表現できる
    * その他jinja2形式の多様な表現ができる

## :package: 0.59.1

:fa-calendar: `2018-12-06`

!!! bug "whenで指定した式にoptionalプロパティが含まれると正しく動かないことがある不具合を修正しました"


## :package: 0.59.0

:fa-calendar: `2018-12-03`

??? info "did_challenge/tagアドオンを追加しました ([did_challenge/tag])"

    * 指定した条件に一致するとき任意の値(パラメータ参照可)でタグを付与できます
    * 詳しくは[did_challenge/tag]をご覧下さい


## :package: 0.58.1

:fa-calendar: `2018-11-29`

??? bug "proxyを指定すると実行できない不具合を修正しました"

    * 該当プロパティは [AccessPoint](http://tadashi-aikawa.github.io/jumeaux/ja/models/access-point/#accesspoint_1) をご覧下さい


## :package: 0.58.0

:fa-calendar: `2018-10-30`

??? danger "出力レポート内の時刻にTimezone情報を追加しました"

    * Jumeaux実行マシンのlocal timezoneに準拠した時刻が記載されます
      * たとえばJSTの場合は`2018-10-30T10:01:28.199299+09:00`です

??? bug "空のpathが含まれるレポートからretryすると期待通り動作しない不具合を修正しました"

    * pathが空の場合に`No Path`という値で上書きしていたのをやめました(空のまま)
        * retry時に`No Path`をpathとしてリクエストしてしまっていたのが原因のため

!!! hint "不要ないくつかの警告を表示しないようにしました"


## :package: 0.57.1

:fa-calendar: `2018-08-04`

??? bug "特定の条件下でretryに失敗する不具合を修正しました"

    以下の条件を満たすとき失敗していました。

    1. Jumeauxの実行結果に整数で表現可能なresponse_secが含まれる (例: response_sec: 2.0 など)
    2. 1のReportをMiroirからダウンロードし、それを入力にして`jumeaux retry`を実行する

    直接の原因は、`report.json`の`response_sec`がint型を受けつけていなかった為です。(floatでなければいけない)  
    2のダウンロード時に2.0のようなfloat型は2のようなint型へ変換されていました。(JavaScriptの仕様と思われる)  
    今回の対応によってint型の場合にfloat型へ変換して処理を続行するようになりました。


## :package: 0.57.0

:fa-calendar: `2018-07-30`

??? info "アクセス先クエリ制御のcase insensitive対応をしました"

    * `/i`を付けることでキーの大文字/小文字を同一視することができます
    * 詳しくは [models/accesspoint] のQueryCustomizationをご覧下さい


## :package: 0.56.0

:fa-calendar: `2018-07-29`

??? info "アクセス先ごとにクエリを制御できるようにしました"

    * OneとOtherそれぞれに対して、上書き(無い場合は追加)と削除の操作が可能です
    * アクセス先情報という位置づけのため、リクエストごとに制御を変更することはできません
    * 設定の詳細は [configuration] から AccessPoint の`query`をご覧ください


## :package: 0.55.2

:fa-calendar: `2018-07-04`

??? hint "PythonPathにJumeaux実行時のカレントディレクトリを追加するようにしました"

    * カレントディレクトリに配置するだけで独自アドオンなどを気軽に使用できるようになります


## :package: 0.55.1

:fa-calendar: `2018-07-02`

??? bug "特定ケースでプロパティに差分が無くてもSameとならない不具合を修正しました"

    * 特定ケースとは **judgementレイヤにアドオンが未指定の場合** です。


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


[configuration]: ../getstarted/configuration
[viewer]: ../getstarted/quickstart/#viewer
[template/#functions]: ../template#functions
[addons]: ../addons
[addons/addon]: ../addons#addon
[log2reqs/plain]: ../addons/log2reqs#plain
[log2reqs/csv]: ../addons/log2reqs#csv
[reqs2reqs/empty_guard]: ../addons/reqs2reqs#empty_guard
[reqs2reqs/filter]: ../addons/reqs2reqs#filter
[reqs2reqs/replace]: ../addons/reqs2reqs#replace
[reqs2reqs/rename]: ../addons/reqs2reqs#rename
[res2res/json]: ../addons/res2res#json
[res2res/json_sort]: ../addons/res2res#json_sort
[res2res/type]: ../addons/res2res#type
[res2dict]: ../addons/res2dict
[res2dict/json]: ../addons/res2dict#json
[res2dict/html]: ../addons/res2dict#html
[res2dict/xml]: ../addons/res2dict#xml
[res2dict/block]: ../addons/res2dict#block
[judgement/ignore]: ../addons/judgement#ignore
[judgement/ignore_properties]: ../addons/judgement#ignore_properties
[judgement/same]: ../addons/judgement#same
[store_criterion/free]: ../addons/store_criterion#free
[dump/xml]: ../addons/dump#xml
[dump/html]: ../addons/dump#html
[dump/json]: ../addons/dump#json
[did_challenge/tag]: ../addons/did_challenge#tag
[final/miroir]: ../addons/final#miroir
[final/slack]: ../addons/final#slack
[final/json]: ../addons/final#json
[final/summary]: ../addons/final#summary
[final/viewer]: ../addons/final#viewer
[models/accesspoint]: ../models/access-point
[models/trial]: ../models/trial
