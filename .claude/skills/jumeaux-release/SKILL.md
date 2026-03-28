---
name: jumeaux-release
description: Jumeauxをリリースするときのみ利用できるスキルです。
allowed-tools:
  - Bash(git pull)
  - Bash(git status)
  - Bash(git log:*)
  - Bash(git tag:*)
  - Bash(make ci)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git push)
  - Bash(gh workflow list)
  - Bash(gh run list:*)
  - Bash(gh run watch:*)
---

## 手順

1. `git pull` をして差分がないことを確認する
    - 差分があったら中断
2. `make ci` を実行する
    - 失敗したら中断
3. `git status` でローカルに差分がないことを確認する
    - 差分があったら中断
4. GitHub Actionsの `Test` が成功していることを確認する
    - 失敗していたら中断
5. `mkdocs/ja/releases` 配下のメジャーバージョン番号に沿ったmdファイルに新しいバージョンのセクションを追加する
6. `git commit -m "chore: v<新しいバージョン>"` とコミットする
7. `git push`
8. `gh workflow run Release --ref master --field version=<新しいバージョン>` の実行をユーザーに依頼する
9. `gh run list --workflow=Release --limit=1` でワークフローが完了したことを確認する
10. `git pull`
