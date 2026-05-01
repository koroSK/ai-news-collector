# AI ニュース自動収集アプリ 仕様書

## 1. 概要

| 項目 | 内容 |
|------|------|
| アプリ名 | AI News Collector |
| リポジトリ | https://github.com/koroSK/ai-news-collector |
| 目的 | AIに関するニュースを毎日自動収集し、GitHubリポジトリに保存する |
| 実行環境 | GitHub Actions（クラウド実行） |
| 作成日 | 2026-05-01 |

---

## 2. 機能仕様

### 2.1 ニュース収集

| 項目 | 内容 |
|------|------|
| 収集ソース | Google News RSS |
| 収集言語 | 英語（6件）・日本語（4件） |
| 収集件数 | 計10件/日（重複排除後） |
| 検索キーワード（英語） | `artificial intelligence AI` |
| 検索キーワード（日本語） | `AI 人工知能` |

### 2.2 重複排除

| 項目 | 内容 |
|------|------|
| 対象 | 日をまたいだ重複（過去に収集済みのURL） |
| 管理ファイル | `seen_urls.json` |
| 判定基準 | 記事のURL |
| 上限件数 | 500件（超過時は古いものから自動削除） |
| 動作 | 収集後に新規URLを追記し、次回実行時にフィルタリング |

### 2.3 実行スケジュール

| 項目 | 内容 |
|------|------|
| 実行タイミング | 毎日 09:00 JST（= UTC 00:00） |
| cron設定 | `0 0 * * *` |
| 手動実行 | GitHub Actions の `workflow_dispatch` から可能 |

### 2.4 保存形式

- **ファイル形式**: Markdown（`.md`）
- **保存先**: リポジトリ内 `news/` ディレクトリ
- **ファイル名**: `YYYY-MM-DD.md`（実行日付）
- **保存内容**:
  - 収集日・件数
  - 英語ニュース一覧（タイトル・ソース・日付・リンク）
  - 日本語ニュース一覧（タイトル・ソース・日付・リンク）

**出力例:**
```
news/
  2026-05-01.md
  2026-05-02.md
  2026-05-03.md
  ...
```

---

## 3. システム構成

```
GitHub Actions（スケジュール実行）
        │
        ▼
news_collector.py
        │
        ├── seen_urls.json を読み込み（収集済みURLを確認）
        │
        ├── Google News RSS（英語）
        │       └── 未収集のみ 上位6件取得
        │
        └── Google News RSS（日本語）
                └── 未収集のみ 上位4件取得
        │
        ▼
重複排除後の記事を news/YYYY-MM-DD.md として保存
        │
        ▼
seen_urls.json を更新
        │
        ▼
GitHub リポジトリへ自動コミット・プッシュ
```

---

## 4. ファイル構成

```
ai-news-collector/
├── .github/
│   └── workflows/
│       └── collect_news.yml   # GitHub Actions ワークフロー定義
├── docs/
│   ├── spec.md                # 本仕様書
│   └── architecture.html      # システムアーキテクチャ図
├── news/
│   └── YYYY-MM-DD.md          # 収集されたニュース（日付ごと）
├── news_collector.py          # ニュース収集スクリプト
├── seen_urls.json             # 収集済みURL履歴（重複排除用）
└── README.md                  # リポジトリ概要
```

---

## 5. 各ファイルの仕様

### 5.1 `news_collector.py`

| 関数 | 役割 |
|------|------|
| `load_seen_urls()` | `seen_urls.json` から収集済みURLリストを読み込む |
| `save_seen_urls(seen)` | 収集済みURLリストを `seen_urls.json` に保存する（500件上限） |
| `fetch_news()` | Google News RSSから未収集の英語・日本語ニュースを取得して返す |
| `save_news(en, ja)` | 取得したニュースをMarkdown形式で `news/` に保存する |

**使用ライブラリ:**
- `feedparser` - RSSフィードの解析
- `datetime` - 日付処理
- `os` - ディレクトリ作成
- `json` - seen_urls.json の読み書き

### 5.2 `seen_urls.json`

| 項目 | 内容 |
|------|------|
| 形式 | JSON配列（URLの文字列リスト） |
| 更新タイミング | 毎回の収集実行後 |
| 上限 | 500件（超過時は先頭から削除） |
| 用途 | 日をまたいだ重複排除 |

### 5.3 `.github/workflows/collect_news.yml`

| 設定項目 | 値 |
|----------|----|
| 実行OS | `ubuntu-latest` |
| Pythonバージョン | `3.11` |
| パーミッション | `contents: write`（リポジトリへの書き込み許可） |
| コミット対象 | `news/` ディレクトリ・`seen_urls.json` |
| コミットユーザー | `github-actions[bot]` |

---

## 6. 依存関係

| ライブラリ | バージョン | 用途 |
|-----------|-----------|------|
| feedparser | 最新版 | RSSフィード解析 |

---

## 7. 制限事項・注意点

- Google News RSSは非公式APIのため、仕様変更により動作しなくなる可能性がある
- 重複排除はURLベースのため、URLが異なる同内容の記事は除外されない
- 収集件数は重複排除後のため、フィード内の新着が少ない場合は10件未満になる場合がある
- `seen_urls.json` の上限（500件）を超えると古いURLから削除されるため、約50日以上前の記事は再収集される可能性がある
- GitHub Actionsの無料枠（月2,000分）の範囲内で動作する（1回あたり約1分）

---

## 8. 今後の拡張案

- [ ] Slack / LINE への通知機能の追加
- [ ] 収集キーワードのカスタマイズ機能
- [ ] タイトルの類似度による重複排除
- [ ] 週次・月次のまとめレポート生成
- [ ] 感情分析・トレンド分析の追加
