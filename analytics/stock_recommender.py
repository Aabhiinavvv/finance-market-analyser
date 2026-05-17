import yfinance as yf
import pandas as pd

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ONGC.NS",
    "ITC.NS",
    "LT.NS"
]


def momentum_score(data):

    if data.empty or len(data) < 20:
        return 0

    price = float(data["Close"].iloc[-1])
    ma20 = float(data["Close"].rolling(20).mean().iloc[-1])

    if price > ma20:
        return 1

    return 0


def volume_spike(data):

    if data.empty or len(data) < 20:
        return 0

    avg_vol = float(data["Volume"].rolling(20).mean().iloc[-1])
    today_vol = float(data["Volume"].iloc[-1])

    if today_vol > avg_vol * 1.5:
        return 1

    return 0


def volatility_score(data):

    if data.empty or len(data) < 20:
        return 0

    returns = data["Close"].pct_change().dropna()

    if returns.empty:
        return 0

    vol = float(returns.std())

    if vol > 0.02:
        return 1

    return 0

def stock_score(ticker):

    data = yf.download(ticker, period="3mo")

    if data.empty:
        return 0

    score = 0

    score += momentum_score(data)
    score += volume_spike(data)
    score += volatility_score(data)

    return score


def recommend_stocks():

    results = []

    for stock in stocks:

        score = stock_score(stock)

        results.append((stock, score))

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results[:5]