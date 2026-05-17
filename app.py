import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from ai.expert_analysis import analyze_event
from analytics.event_detector import detect_event, predict_impact
import yfinance as yf
from analytics.event_detector import advanced_event_prediction
from analytics.stock_recommender import recommend_stocks
from ai.market_analyst import analyze_market
from analytics.fundamental_screener import analyze_stock
from ai.financial_explainer import explain_stock
from analytics.shareholding import get_shareholding

from news import get_news

from ml.prediction import predict_stock
from ai.chatbot import ask_finance

def normalize_ticker(ticker):
    ticker = ticker.upper().strip()

    if ticker.endswith(".NS"):
        return ticker

    return ticker + ".NS"


st.set_page_config(layout="wide")

st.title("📊 Finance Dashboard")

ticker_input = st.text_input("Enter Stock Ticker", "RELIANCE")

ticker = normalize_ticker(ticker_input)

data = yf.download(ticker, period="6mo")

if data.empty:
    st.error("Invalid stock ticker")
else:
    st.write(f"Showing data for: {ticker}")
    st.line_chart(data["Close"])

if data.empty:
    st.error("Invalid ticker or no data found.")
    st.stop()

import yfinance as yf

@st.cache_data(ttl=300)
def safe_price(symbol):

    try:
        data = yf.Ticker(symbol).history(period="1d")

        if data.empty:
            return "N/A"

        return round(data["Close"].iloc[-1], 2)

    except:
        return "N/A"


nifty = safe_price("^NSEI")
sensex = safe_price("^BSESN")
usd = safe_price("INR=X")
gold = safe_price("GC=F")
crude = safe_price("CL=F")

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric("NIFTY50", nifty)
col2.metric("SENSEX", sensex)
col3.metric("USD/INR", usd)
col4.metric("Gold", gold)
col5.metric("Crude Oil", crude)


# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10= st.tabs([
    "📈 Stock Price",
    "🔮 Prediction",
    "📰 Market News",
    "📊 Stock Screener",
    "🤖 AI Chat",
    "🧠 Expert Analysis",
    "🤖 Ask anything about markets",
    "⚡ Event Impact Detector",
    "🤖 AI Stock Recommendation Engine",
    "🧠 Autonomous Market Analyst"
])

# -----------------------------
# Stock Price
# -----------------------------
with tab1:

    st.subheader("Stock Price")

    # -----------------------------
    # 📅 Time Selector
    # -----------------------------
    period_map = {
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "1Y": "1y",
        "5Y": "5y",
        "10Y": "10y",
        "MAX": "max"
    }

    selected = st.selectbox("Select Range", list(period_map.keys()))

    # -----------------------------
    # 📊 Download Data (FIRST)
    # -----------------------------
    data = yf.download(ticker, period=period_map[selected])

    if data.empty:
        st.error("No data found")
        st.stop()

    close_price = data["Close"]

    # -----------------------------
    # 📈 Plot
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=close_price,
        mode="lines",
        name="Close Price",
        line=dict(color="cyan", width=2)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title=f"{ticker} Price ({selected})"
    )

    st.plotly_chart(fig, width="stretch")

# -----------------------------
# Prediction
# -----------------------------
with tab2:

    st.subheader("Prediction")

    prediction = predict_stock(data)

    st.metric(
        label="Next Day Prediction",
        value=prediction
    )

# -----------------------------
# News
# -----------------------------
with tab3:

    st.subheader("Market News")

    articles = get_news()

    if not articles:
        st.info("News service is currently unavailable. Please check your internet/DNS or try again later.")

    for article in articles:

        st.markdown(f"### {article['title']}")

        if article["description"]:
            st.write(article["description"])

        st.markdown("---")

# -----------------------------
# Screener
# -----------------------------
with tab4:

    st.subheader("🧠 AI Smart Stock Screener")

    ticker_search = st.text_input("Search Stock (TCS, RELIANCE, INFY)")

    if ticker_search:

        ticker = ticker_search.upper().strip()

        if not ticker.endswith(".NS"):
            ticker = ticker + ".NS"

        data = yf.download(
            ticker,
            period="6mo",
            auto_adjust=False,
            progress=False
        )

        if data.empty:
            st.error("Invalid stock")
            st.stop()

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price"
        ))

        data["MA20"] = data["Close"].rolling(20).mean()

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

        st.plotly_chart(fig, use_container_width=True)


        fig.update_layout(template="plotly_dark", height=400)

        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # 📊 Fundamental Data
        # -----------------------------
        overview, pros, cons, financials, balance, cashflow ,quarterly= analyze_stock(ticker)

        # -----------------------------
        # 🔥 AI SUMMARY CARDS
        # -----------------------------
        st.markdown("## 📊 AI Summary")

        col1, col2, col3, col4 = st.columns(4)

        roe = overview.get("ROE", 0) or 0
        pe = overview.get("PE Ratio", 0) or 0

        growth = "Strong" if roe > 0.2 else "Moderate"
        valuation = "Cheap" if pe and pe < 20 else "Expensive"
        risk = "Low" if pe < 25 else "Medium"
        verdict = "BUY" if roe > 0.2 else "HOLD"

        col1.metric("Growth", growth)
        col2.metric("Valuation", valuation)
        col3.metric("Risk", risk)
        col4.metric("Verdict", verdict)

        # -----------------------------
        # 📊 Overview
        # -----------------------------
        st.markdown("## 📊 Overview")
        st.dataframe(overview)

        # -----------------------------
        # ✔ Pros / Cons
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Pros")
            for p in pros:
                st.write("✔", p)

        with col2:
            st.markdown("### ⚠ Cons")
            for c in cons:
                st.write("⚠", c)


        st.markdown("## 🧾 Shareholding Pattern")

        share = get_shareholding(ticker_search)

        if share:
            st.dataframe(share)
        else:
            st.warning("No shareholding data found")


                # -----------------------------
        # 📊 Profit & Loss
        # -----------------------------
        st.markdown("## 📊 📈 Profit & Loss")

        if not financials.empty:
            st.dataframe(financials.T)
        else:
            st.warning("No data available")

        # -----------------------------
        # 📉 Balance Sheet
        # -----------------------------
        st.markdown("## 📉 Balance Sheet")

        if not balance.empty:
            st.dataframe(balance.T)
        else:
            st.warning("No data available")

        # -----------------------------
        # 💰 Cash Flow
        # -----------------------------
        st.markdown("## 💰 Cash Flow")

        if not cashflow.empty:
            st.dataframe(cashflow.T)
        else:
            st.warning("No data available")

        # -----------------------------
        # 📊 Quarterly Results
        # -----------------------------
        st.markdown("## 📊 Quarterly Results")

        if not quarterly.empty:
            st.dataframe(quarterly.T)

            if "Total Revenue" in quarterly.index:
                st.line_chart(quarterly.loc["Total Revenue"])

            if "Net Income" in quarterly.index:
                st.line_chart(quarterly.loc["Net Income"])
        else:
            st.warning("No quarterly data available")




        # -----------------------------
        # 🧠 AI ANALYSIS
        # -----------------------------
        st.markdown("## 🤖 AI Analysis")

        try:
            explanation = explain_stock(ticker, overview, pros, cons)
            st.write(explanation)
        except:
            st.warning("AI analysis unavailable")

        # -----------------------------
        # 📊 Peer Comparison
        # -----------------------------
        st.markdown("## 📊 Peer Comparison")

        peers = ["TCS.NS", "INFY.NS", "WIPRO.NS"]

        peer_data = []

        for p in peers:
            info = yf.Ticker(p).info
            peer_data.append({
                "Stock": p,
                "PE": info.get("trailingPE"),
                "ROE": info.get("returnOnEquity")
            })

        st.dataframe(peer_data)

        # -----------------------------
        # 📉 Financial Trends
        # -----------------------------
        st.markdown("## 📈 Revenue Trend")

        if not financials.empty:
            try:
                revenue = financials.loc["Total Revenue"]
                st.line_chart(revenue)
            except:
                st.write("No revenue data")

        # -----------------------------
        # 🔥 FINAL VERDICT
        # -----------------------------
        st.markdown("## 🔥 Final Verdict")

        st.write(f"""
✔ Growth: {growth}  
✔ Valuation: {valuation}  
✔ Risk: {risk}  

👉 Recommendation: {verdict}
""")

# -----------------------------
# AI Finance Chat
# -----------------------------
with tab5:

    st.subheader("Ask AI About Markets")

    question = st.text_input("Ask a finance question")

    if question:

        answer = ask_finance(question)

        st.write(answer)

# AI Market Explanation
        

with tab6:

    st.subheader("Expert Analysis")

    news_input = st.text_area("Enter financial news")

    if st.button("Analyze News"):

        result = analyze_event(news_input)

        st.markdown("### Expert Analysis")
        st.write(result)

with tab7:

    st.subheader("AI Market Explanation")

    question = st.text_input("Ask about this stock")

    if question:

        prompt = f"""
Stock: {ticker}

Recent price:
{data.tail(5)}

Explain the market movement and possible reasons.
"""

        answer = ask_finance(prompt)

        st.write(answer)

from analytics.event_detector import detect_event, predict_impact

with tab8:

    st.subheader("Event Impact Predictor")

    news = st.text_area("Enter global event")

    if st.button("Predict Impact"):

        event = detect_event(news)

        predictions = advanced_event_prediction(event)

        st.write("Detected Event:", event)

        if predictions:

            for stock, score in predictions:
                st.write(stock, "Impact Score:", score)

        else:
            st.warning("No predicted impact for this event.")


with tab9:

    st.subheader("🤖 AI Stock Recommendation Engine")

    if st.button("Find Stocks"):

        results = recommend_stocks()

        for stock, score in results:

            st.write(stock, "Signal Score:", score)

with tab10:

    st.subheader("Autonomous AI Market Analyst")

question = st.text_input("Ask about markets")

if question:
    event, stocks = analyze_market(question)

    st.markdown(f"### Detected Event: **{event.title()}**")

    st.markdown("### Top Stocks to Watch")

    stock_data = []

    for stock, score in stocks:
        stock_data.append({
            "Stock": stock,
            "Signal Score": score
        })

    st.table(stock_data)

           


st.markdown("## 📊 AI Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Growth", "Strong")
col2.metric("Valuation", "Fair")
col3.metric("Risk", "Low")
col4.metric("Verdict", "BUY")

