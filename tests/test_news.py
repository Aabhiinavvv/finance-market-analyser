from unittest.mock import patch

from news import get_news


def test_news_returns_empty_when_key_is_missing(monkeypatch):
    monkeypatch.delenv("NEWSAPI_KEY", raising=False)
    assert get_news() == []


def test_news_returns_limited_articles(monkeypatch):
    monkeypatch.setenv("NEWSAPI_KEY", "test-key")

    fake_articles = [{"title": str(i)} for i in range(10)]

    with patch("news.NewsApiClient") as client_cls:
        client_cls.return_value.get_top_headlines.return_value = {
            "articles": fake_articles
        }
        result = get_news(limit=3)

    assert len(result) == 3
    assert result[0]["title"] == "0"
