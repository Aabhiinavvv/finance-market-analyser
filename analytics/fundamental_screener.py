import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from ai.financial_explainer import explain_stock

import pandas as pd
import yfinance as yf



stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "LT.NS",
    "ONGC.NS"
]


def run_screener():

    results = []

    for stock in stocks:

        try:
            data = yf.download(stock, period="3mo")

            if data.empty or len(data) < 20:
                continue

            close = data["Close"]

            price = float(close.iloc[-1])
            ma20 = float(close.rolling(20).mean().iloc[-1])
            
            trend = "Bullish" if price > ma20 else "Bearish"
            results.append({
                
                "Stock": stock,
                "Price": round(price, 2),
                "MA20": round(ma20, 2),
                "Trend": trend
            })

        except:
            continue

    df = pd.DataFrame(results)

    return df


def get_candlestick_chart(ticker):
    ticker = normalize_ticker(ticker)

    data = yf.download(
        ticker,
        period="6mo",
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        return None

    # Fix yfinance MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna(subset=["Open", "High", "Low", "Close"])

    if data.empty:
        return None

    data["MA20"] = data["Close"].rolling(20).mean()

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA20"],
        line=dict(color="orange", width=2),
        name="MA20"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_rangeslider_visible=False,
        title=f"{ticker} Price Chart"
    )

    return fig






def analyze_stock(ticker):

    ticker = ticker.upper() + ".NS"

    stock = yf.Ticker(ticker)
    info = stock.info

    overview = {
        "Market Cap": info.get("marketCap"),
        "PE Ratio": info.get("trailingPE"),
        "ROE": info.get("returnOnEquity"),
        "Dividend Yield": info.get("dividendYield"),
        "Debt to Equity": info.get("debtToEquity"),
        "Profit Margin": info.get("profitMargins"),
        "book":info.get("bookvalue"),
    }

    financials = stock.financials
    balance = stock.balance_sheet
    cashflow = stock.cashflow
    quarterly = stock.quarterly_financials

    pros = []
    cons = []

    roe = info.get("returnOnEquity", 0)
    pe = info.get("trailingPE", 0)
    debt = info.get("debtToEquity", 0)

    if roe and roe > 0.2:
        pros.append("High ROE")

    if pe and pe < 20:
        pros.append("Reasonable valuation")

    if debt and debt > 100:
        cons.append("High debt")

    if len(pros) == 0:
        pros.append("No strong positives")

    if len(cons) == 0:
        cons.append("No major negatives")

    return overview, pros, cons, financials, balance, cashflow,quarterly 
