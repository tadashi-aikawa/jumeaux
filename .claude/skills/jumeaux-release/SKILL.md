---
name: jumeaux-release
description: Jumeauxをリリースするときのみ利用できるスキルです。
allowed-tools:
  - Bash(git pull)
  - Bash(git push)
  - Bash(make ci)
  - Bash(git commit:*)
---

## 手順

1. `git pull` をして差分がないことを確認する
    - 差分があったら中断
2. `make ci` を実行する
    - 失敗したら中断
3. `git status` でローカルに差分がないことを確認する
    - 差分があったら中断
4. GitHub Actionsの `test` が成功していることを確認する
    - 失敗していたら中断
5. `mkdocs/ja/releases` 配下のメジャーバージョン番号に沿ったmdファイルに新しいバージョンのセクションを追加する
6. `git commit -m "chore: v<新しいバージョン>"` とコミットする
7. `git push`
8. GitHub Actionsの `release` を実行する
9. https://pypi.org/project/jumeaux/ に最新バージョンがリリースされたことを確認する

