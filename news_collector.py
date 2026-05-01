import feedparser
import datetime
import os

FEEDS = [
    ("en", "https://news.google.com/rss/search?q=artificial+intelligence+AI&hl=en-US&gl=US&ceid=US:en"),
    ("ja", "https://news.google.com/rss/search?q=AI+人工知能&hl=ja&gl=JP&ceid=JP:ja"),
]

def fetch_news():
    en_articles, ja_articles = [], []

    for lang, url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "不明"),
                "lang": lang,
            }
            if lang == "en":
                en_articles.append(article)
            else:
                ja_articles.append(article)

    return en_articles[:6], ja_articles[:4]

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

    print(f"✅ 保存完了: {filepath}")
    return filepath

if __name__ == "__main__":
    en, ja = fetch_news()
    save_news(en, ja)
