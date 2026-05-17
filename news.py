from newsapi import NewsApiClient
import os

def get_news():
    api_key = os.getenv("NEWSAPI_KEY", "60a1865e92364a25adedd5f1f3e9fdd5")

    try:
        newsapi = NewsApiClient(api_key=api_key)

        articles = newsapi.get_top_headlines(
            category="business",
            language="en"
        )

        return articles.get("articles", [])[:5]
    except Exception:
        # DNS/network failures should not crash the app.
        return []