# CLAUDE

## コミットメッセージ

Conventional Commits 形式で日本語で書く。

### フォーマット

```
<type>(<scope>): <description>
```

- `type`: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`, `build`, `ci`, `test`
  - 破壊的変更がある場合は `feat!` のように `!` を付ける
- `scope`: `timer_engine`, `ui_panel`, `alert`, `persistence` など機能単位 (省略可)
- `description`: ユーザー視点で何が変わったかを簡潔に書く

### description の書き方

- ユーザーにとって何が変わるかを書く (実装詳細ではなく体験の変化)
- 「〜を追加」「〜を修正」「〜に変更」のように結果を述べる
- 内部的なリファクタリングの場合のみ実装視点で書いてよい

## ユニットテスト実行

```bash
make test
```

## E2Eテスト実行

```bash
make test-e2e
```

