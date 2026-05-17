from transformers import pipeline
import yfinance as yf

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "oil supply shock",
    "interest rate change",
    "inflation surge",
    "technology breakthrough",
    "geopolitical tension",
    "government regulation"
]


def detect_event(question):
    result = classifier(question, labels)
    return result["labels"][0]


sector_map = {
    "oil supply shock": {
        "positive": ["energy"],
        "negative": ["airlines"]
    },
    "interest rate change": {
        "positive": ["banks"],
        "negative": ["real estate"]
    },
    "inflation surge": {
        "positive": ["commodities"],
        "negative": ["consumer"]
    },
    "geopolitical tension": {
        "positive": ["defence", "oil & gas", "metals"],
        "negative": ["aviation", "paint", "auto"]
    },
}


sector_stocks = {
    "defence": [
        ("HAL", "HAL.NS"),
        ("BEL", "BEL.NS"),
        ("Bharat Dynamics", "BDL.NS"),
    ],
    "oil & gas": [
        ("ONGC", "ONGC.NS"),
        ("Oil India", "OIL.NS"),
        ("Reliance", "RELIANCE.NS"),
    ],
    "metals": [
        ("Tata Steel", "TATASTEEL.NS"),
        ("Hindalco", "HINDALCO.NS"),
        ("JSW Steel", "JSWSTEEL.NS"),
    ],
}


def stock_signal(ticker):
    data = yf.download(ticker, period="3mo", progress=False)

    if data.empty:
        return 0

    close = data["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    price = float(close.iloc[-1])
    ma20 = float(close.rolling(20).mean().iloc[-1])

    score = 0

    if price > ma20:
        score += 1

    return score


def analyze_market(question):
    event = detect_event(question)

    sectors = sector_map.get(event, {})
    results = []

    for sector in sectors.get("positive", []):
        stocks = sector_stocks.get(sector, [])

        for stock_name, ticker in stocks:
            score = stock_signal(ticker)
            results.append((stock_name, score))

    if len(results) == 0:
        results = [
            ("Reliance", 70),
            ("HDFC Bank", 68),
            ("ICICI Bank", 66),
            ("TCS", 64),
            ("Larsen & Toubro", 62),
        ]

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return event, results[:5]
