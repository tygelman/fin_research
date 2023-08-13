import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt


def main():
    st.title("Technical Analysis")

    stock_ticker = st.text_input("Enter a stock ticker", "AAPL")
    start_date = st.date_input("Enter a start date")
    end_date = st.date_input("Enter an end date")

    if st.button("Show Technical Analysis"):
        df = download_data(stock_ticker, start_date, end_date)
        df = add_technical_indicators(df)
        display_technical_analysis(df)


def download_data(stock_ticker, start_date, end_date):
    df = yf.download(stock_ticker, start=start_date, end=end_date)
    return df


def add_technical_indicators(df):
    df["SMA_50"] = ta.trend.SMAIndicator(df["Close"], window=50).sma_indicator()
    df["SMA_200"] = ta.trend.SMAIndicator(df["Close"], window=200).sma_indicator()
    df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()
    df["Chaikin Money Flow"] = ta.volume.ChaikinMoneyFlowIndicator(
        df["High"], df["Low"], df["Close"], df["Volume"]
    ).chaikin_money_flow()
    return df


def display_technical_analysis(df):
    st.write("### Technical Analysis")

    # Simple Moving Averages (SMA)
    st.write("#### Simple Moving Averages (SMA)")
    st.line_chart(df[["Close", "SMA_50", "SMA_200"]], use_container_width=True)
    st.write("SMA 50 and SMA 200 are commonly used trend-following indicators.")

    # Exponential Moving Average (EMA)
    st.write("#### Exponential Moving Average (EMA)")
    st.line_chart(df[["Close", "EMA_20"]], use_container_width=True)
    st.write(
        "EMA gives more weight to recent prices and is sensitive to price changes."
    )

    # Relative Strength Index (RSI)
    st.write("#### Relative Strength Index (RSI)")
    st.line_chart(df[["RSI"]], use_container_width=True)
    st.write(
        "RSI measures the speed and change of price movements. Values above 70 indicate overbought conditions, while values below 30 indicate oversold conditions."
    )

    # Moving Average Convergence Divergence (MACD)
    st.write("#### Moving Average Convergence Divergence (MACD)")
    st.line_chart(df[["MACD"]], use_container_width=True)
    st.write(
        "MACD consists of the MACD line, signal line, and histogram. It helps identify potential trend reversals."
    )

    # Chaikin Money Flow
    st.write("#### Chaikin Money Flow")
    st.line_chart(df[["Chaikin Money Flow"]], use_container_width=True)
    st.write(
        "Chaikin Money Flow measures the accumulation/distribution of money flow in a stock. Positive values suggest buying pressure."
    )


if __name__ == "__main__":
    main()
