import feedparser
import datetime
import os
import json

FEEDS = [
    ("en", "https://news.google.com/rss/search?q=artificial+intelligence+AI&hl=en-US&gl=US&ceid=US:en"),
    ("ja", "https://news.google.com/rss/search?q=AI+人工知能&hl=ja&gl=JP&ceid=JP:ja"),
]

SEEN_URLS_FILE = "seen_urls.json"
MAX_SEEN_URLS = 500  # 肥大化防止のため古いURLを自動削除する上限


def load_seen_urls():
    if not os.path.exists(SEEN_URLS_FILE):
        return []
    with open(SEEN_URLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_seen_urls(seen):
    # 上限を超えたら古いものから削除
    if len(seen) > MAX_SEEN_URLS:
        seen = seen[-MAX_SEEN_URLS:]
    with open(SEEN_URLS_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)


def fetch_news():
    seen_urls = load_seen_urls()
    seen_set = set(seen_urls)

    en_articles, ja_articles = [], []

    for lang, url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link = entry.get("link", "")
            if link in seen_set:
                continue
            article = {
                "title": entry.get("title", ""),
                "link": link,
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "不明"),
                "lang": lang,
            }
            if lang == "en":
                en_articles.append(article)
            else:
                ja_articles.append(article)

    en_articles = en_articles[:6]
    ja_articles = ja_articles[:4]

    # 今回収集したURLをseen_urlsに追加して保存
    new_urls = [a["link"] for a in en_articles + ja_articles]
    save_seen_urls(seen_urls + new_urls)

    return en_articles, ja_articles


def save_news(en_articles, ja_articles):
    today = datetime.date.today().strftime("%Y-%m-%d")
    os.makedirs("news", exist_ok=True)
    filepath = f"news/{today}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 📰 AI ニュース - {today}\n\n")
        f.write(f"> 収集件数: 英語 {len(en_articles)} 件 / 日本語 {len(ja_articles)} 件\n\n")
        f.write("---\n\n")

        f.write("## 🌐 英語ニュース\n\n")
        for i, a in enumerate(en_articles, 1):
            f.write(f"### {i}. {a['title']}\n\n")
            f.write(f"- **ソース**: {a['source']}\n")
            f.write(f"- **日付**: {a['published']}\n")
            f.write(f"- **リンク**: [{a['title']}]({a['link']})\n\n")

        f.write("---\n\n")
        f.write("## 🇯🇵 日本語ニュース\n\n")
        for i, a in enumerate(ja_articles, 1):
            f.write(f"### {i}. {a['title']}\n\n")
            f.write(f"- **ソース**: {a['source']}\n")
            f.write(f"- **日付**: {a['published']}\n")
            f.write(f"- **リンク**: [{a['title']}]({a['link']})\n\n")

    print(f"✅ 保存完了: {filepath}（英語 {len(en_articles)} 件 / 日本語 {len(ja_articles)} 件）")
    return filepath


if __name__ == "__main__":
    en, ja = fetch_news()
    save_news(en, ja)
