import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

from news import get_news
from analytics.screener import run_screener
from ml.prediction import predict_stock
from ai.chatbot import ask_finance

st.set_page_config(layout="wide")

st.title("📊 AI Finance Dashboard")

ticker = st.text_input("Enter Stock Ticker", "RELIANCE")

# convert to NSE format
if not ticker.endswith(".NS"):
    ticker = ticker.upper() + ".NS"

# download stock data
data = yf.download(ticker, period="3mo")

if data.empty:
    st.error("Invalid ticker or no data found.")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Stock Price",
    "🔮 Prediction",
    "📰 Market News",
    "📊 Stock Screener",
    "🤖 AI Finance Chat"
])

# -----------------------------
# Stock Price
# -----------------------------
with tab1:

    st.subheader("Stock Price")

    close_price = data["Close"].squeeze()

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
        title=f"{ticker} Price (Last 3 Months)"
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

    for article in articles:

        st.markdown(f"### {article['title']}")

        if article["description"]:
            st.write(article["description"])

        st.markdown("---")

# -----------------------------
# Screener
# -----------------------------
with tab4:

    st.subheader("Stock Screener")

    screen = run_screener()

    st.dataframe(screen)

# -----------------------------
# AI Finance Chat
# -----------------------------
with tab5:

    st.subheader("Ask AI About Markets")

    question = st.text_input("Ask a finance question")

    if question:

        answer = ask_finance(question)

        st.write(answer)