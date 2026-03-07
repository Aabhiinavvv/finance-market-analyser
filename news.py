from newsapi import NewsApiClient

def get_news():

    newsapi = NewsApiClient(api_key="60a1865e92364a25adedd5f1f3e9fdd5")

    articles = newsapi.get_top_headlines(
        category="business",
        language="en"
    )

    return articles["articles"][:5]