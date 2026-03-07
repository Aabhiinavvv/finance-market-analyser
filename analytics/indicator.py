
import ta

def add_indicators(df):

    df["RSI"] = ta.momentum.rsi(df["Close"])

    df["MACD"] = ta.trend.macd(df["Close"])

    df["Volatility"] = df["Close"].pct_change().rolling(20).std()

    return df