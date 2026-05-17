from transformers import pipeline
import yfinance as yf
import pandas as pd

from analytics.historical_events import historical_events
from analytics.sector_correlation import sector_movement


# NLP model
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

# Event categories
labels = [
    "oil supply shock",
    "war or geopolitical tension",
    "interest rate change",
    "inflation shock",
    "technology breakthrough",
    "government regulation"
]

# Sector mapping
impact_map = {

    "oil supply shock": {
        "positive": ["ONGC", "RELIANCE", "OIL"],
        "negative": ["INDIGO", "SPICEJET", "ASIANPAINT"]
    },

    "war or geopolitical tension": {
        "positive": ["HAL", "BEL"],
        "negative": ["INDIGO", "ADANIPORTS"]
    },

    "interest rate change": {
        "positive": ["HDFCBANK", "ICICIBANK"],
        "negative": ["DLF", "GODREJPROP"]
    },

    "inflation shock": {
        "positive": ["ITC"],
        "negative": ["DMART", "HINDUNILVR"]
    }
}


def detect_event(news):

    result = classifier(news, labels)

    return result["labels"][0]




def calculate_correlation(stock, benchmark):

    data1 = yf.download(stock, period="1y")["Close"]
    data2 = yf.download(benchmark, period="1y")["Close"]

    df = pd.concat([data1, data2], axis=1).dropna()

    # Step 2 fix
    if df.empty or len(df) < 10:
        return 0

    corr = df.corr().iloc[0,1]

    return float(corr)

def impact_score(correlation, sector_trend):

    correlation = float(correlation)
    sector_trend = float(sector_trend)

    score = correlation * 0.7 + sector_trend * 0.3

    return round(score,2)


def advanced_event_prediction(event):

    sector_data = sector_movement()

    result = []

    if event in historical_events:

        stocks = historical_events[event]["positive"]

        for stock in stocks:

            corr = calculate_correlation(stock, "CL=F")

            sector = "energy"

            sector_trend = sector_data.get(sector,0)

            score = impact_score(corr, sector_trend)

            result.append((stock, score))

    return sorted(result, key=lambda x: float(x[1]), reverse=True)

    for stock in stocks:

        corr = calculate_correlation(stock, "CL=F")

        sector = "energy"

        sector_trend = sector_data.get(sector, 0)

        score = impact_score(corr, sector_trend)

        result.append((stock, score))

    return sorted(result, key=lambda x: float(x[1]), reverse=True)
    
    if len(result) == 0:
        return []

    return sorted(result, key=lambda x: float(x[1]), reverse=True)

def predict_impact(event):

    if event in impact_map:

        return impact_map[event]

    return {"positive": [], "negative": []}