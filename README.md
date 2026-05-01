# 📰 AI News Collector

AIに関するニュースを毎日自動収集してMarkdown形式で保存するリポジトリです。

## 概要

GitHub Actionsを使ってGoogle News RSSからAI関連ニュースを毎朝9時（JST）に自動収集します。過去に収集済みの記事は重複排除されるため、常に新鮮なニュースのみが保存されます。

## 収集内容

| 項目 | 内容 |
|------|------|
| 収集ソース | Google News RSS |
| 英語ニュース | 6件 / 日 |
| 日本語ニュース | 4件 / 日 |
| 実行タイミング | 毎朝 9:00 JST |
| 重複排除 | 過去収集済みURLをスキップ |

## ファイル構成

```
ai-news-collector/
├── .github/
│   └── workflows/
│       └── collect_news.yml   # GitHub Actions ワークフロー
├── docs/
│   ├── spec.md                # 仕様書
│   └── architecture.html      # システムアーキテクチャ図
├── news/
│   └── YYYY-MM-DD.md          # 収集されたニュース（日付ごと）
├── news_collector.py          # ニュース収集スクリプト
├── seen_urls.json             # 収集済みURL履歴（重複排除用）
└── README.md                  # 本ファイル
```

## 手動実行

GitHub Actions の「Actions」タブ →「Daily AI News Collector」→「Run workflow」から手動で実行できます。

## ドキュメント

- [仕様書](docs/spec.md)
- [システムアーキテクチャ図](docs/architecture.html)
