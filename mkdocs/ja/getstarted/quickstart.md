Quickstart
==========

:fa-desktop: Requirements
-------------------------

以下の環境いずれかが必要です。

* Python3.6以上(推奨)
* Docker


:fa-download: Installation
--------------------------

### Python3.6以上(推奨)

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
* 結果は設定ファイルの[response_dir]で指定したディレクトリ配下に作成されます
    * 実行時に生成されたキー(ユニークなハッシュ)に基づいた名称のディレクトリが作成されます

!!! info "標準出力"

    特定のアドオンが標準出力を使用することがあります。

!!! note

    `--config`を指定しないと`config.yml`が設定されたことになります。
    つまり、`jumeaux run requests`は以下のコマンドと等価です。

    ```
    $ jumeaux run requests --config config.yml
    ```

[response_dir]: https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/configuration/#outputsummary

