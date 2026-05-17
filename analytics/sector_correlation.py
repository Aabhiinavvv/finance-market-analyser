import yfinance as yf
import pandas as pd

# sector proxies
sector_map = {
    "energy": ["ONGC.NS", "RELIANCE.NS"],
    "airlines": ["INDIGO.NS"],
    "banking": ["HDFCBANK.NS", "ICICIBANK.NS"],
    "it": ["TCS.NS", "INFY.NS"]
}

def sector_movement():

    sector_change = {}

    for sector, stocks in sector_map.items():

        changes = []

        for stock in stocks:

            data = yf.download(stock, period="5d")

            if not data.empty:
                change = (data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]
                changes.append(change)

        if len(changes) > 0:
            sector_change[sector] = sum(changes)/len(changes)

    return sector_change