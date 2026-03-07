import feedparser

def get_news():

    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^NSEI"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:10]:

        articles.append({
            "title": entry.title,
            "summary": entry.summary
        })

    return articles