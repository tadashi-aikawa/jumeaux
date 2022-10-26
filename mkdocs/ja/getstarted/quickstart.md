Quickstart
==========

:fa-desktop: Requirements
-------------------------

以下の環境いずれかが必要です。

* Python3.7以上
* Docker


:fa-download: Installation
--------------------------

### Python3.7以上

```
$ pip install jumeaux
```

`jumeaux --version`でバージョンが表示されればOKです。

### Docker

```
$ git clone https://github.com/tadashi-aikawa/jumeaux.git
$ cd jumeaux
$ docker build -t tadashi-aikawa/jumeaux .
```

`docker run -it tadashi-aikawa/jumeaux --version`でバージョンが表示されればOKです。

!!! warning

    以降はPythonの場合を想定して説明します。
    つまり `jumeaux` => `docker run -v (pwd):/tmp -it tadashi-aikawa/jumeaux` とコマンドを置き換えてください。


:fa-file: Create files
----------------------

Jumeauxを実行するには、以下2つのファイルを用意する必要があります。

| ファイル名 |              役割              |              備考               |
| ---------- | ------------------------------ | ------------------------------- |
| config.yml | 設定ファイル                   | 任意のファイルを1つ以上指定可能 |
| requests   | リクエストが記載されたファイル | 任意のファイルを1つ以上指定可能 |

上記ファイルの作成に`jumeaux init`コマンドを使用できます。

```
$ jumeaux init simple
```

`simple`は作成するファイルの種類です。

!!! note

    `jumeaux init help`コマンドで`simple`以外の有効な値を確認できます。


:fa-server: Run mock server
---------------------------

`jumeaux init`コマンドでは上記2ファイルの他に`api`ディレクトリが作成されます。  
`api`ディレクトリの中には、`jumeaux init`で指定したファイルの種類に応じて確認用のダミーhttpレスポンスが作成されます。

`jumeaux server`コマンドを実行すると、カレントディレクトをWebサーバとして起動できます。  
ローカル環境で動作確認をするため、`jumeaux server`コマンドを実行しましょう。


:fa-play-circle: Execute
------------------------

`config.yml`と`requests`を指定して実行しましょう。

```
$ jumeaux run requests
```

* デフォルトでは標準出力に何も出力されません :fa-info-circle:
* 標準エラー出力にはログまたはエラーが出力されます

!!! info "標準出力"

    特定のアドオンが標準出力を使用することがあります。

!!! note

    `--config`を指定しないと`config.yml`が設定されたことになります。
    つまり、`jumeaux run requests`は以下のコマンドと等価です。

    ```
    $ jumeaux run requests --config config.yml
    ```


:fa-laptop: Check
-----------------

結果は設定ファイルの[response_dir]で指定したディレクトリ配下に作成されます。
配下には、実行ごとに生成されるユニークなハッシュに基づいたディレクトリが存在します。

また最も新しい結果にはlatestのシンボリックリンクが貼られます。

```
responses/
├── latest -> 057e69de9677f2694a9bf4e43b6229920554cfdfe3a30c915034919cb048fa16  # 最新の結果へのシンボリックリンク
└── 057e69de9677f2694a9bf4e43b6229920554cfdfe3a30c915034919cb048fa16
    ├── index.html       # Localサーバを立ち上げてアクセスすると結果をGUIで確認できる
    ├── one              # oneで指定したhostのリクエスト結果. simpleの場合は差分アリの結果だけ保存している
    │   └── (2)2
    ├── one-props        # oneの結果をプロパティとして解析した結果を保存している. 結果がjsonの場合はほぼ同じ
    │   └── (2)2.json
    ├── other            # otherで指定したhostのリクエスト結果. simpleの場合は差分アリの結果だけ保存している
    │   └── (2)2
    ├── other-props      # otherの結果をプロパティとして解析した結果を保存している. 結果がjsonの場合はほぼ同じ
    │   └── (2)2.json
    └── report.json  # 結果のjson. index.htmlもこれを参照している
```


### GUIで結果を確認する

`jumeaux viewer`コマンドを実行している場合は以下いずれかのURLにアクセスすると、Viewerで結果を確認することができます。

* http://localhost:5500/responses/latest
* http://localhost:5500/responses/057e69de9677f2694a9bf4e43b6229920554cfdfe3a30c915034919cb048fa16

!!! hint "他の結果も確認してみよう"

    `jumeaux init`コマンドで`ignore_order`のテンプレートを使った結果も確認してみましょう。

!!! hint "GUIでより高度な確認をしたい場合は.."

    [Miroir]の使用を検討してみましょう。`final/miroir`アドオンを使用するとJumeauxの結果を登録することができます。


[response_dir]: ../configuration/#outputsummary
[miroir]: https://github.com/tadashi-aikawa/miroir


### Viewerを開いたまま最新の結果を自動リロードする

`jumeaux viewer`コマンドを実行中は、最新の結果に限り速やかに確認することができます。  
responsesに結果が1つ以上格納された状態で`jumeaux viewer`を実行してみましょう。

自動でブラウザのタブが開き、Viewerが表示されます。

この状態で`jumeaux run`を実行すると、ブラウザのViewerが自動で新しい結果にリロードされます。

!!! hint "リロードのトリガーになるものは?"

    `latest/report.json`に変更があった場合にリロードされます。  
    そのため`jumeaux`を実行せずにシンボリックリンクを切り替えたり、`report.json`を編集しても自動リロードされます。

