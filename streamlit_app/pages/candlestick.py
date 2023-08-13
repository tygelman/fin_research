import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


def main():
    st.title("Candlestick Chart")

    stock_ticker = st.text_input("Enter a stock ticker", "AAPL")
    start_date = st.date_input("Enter a start date")
    end_date = st.date_input("Enter an end date")

    if st.button("Show Candlestick Chart"):
        df = download_data(stock_ticker, start_date, end_date)
        plot_candlestick_chart(df)


def download_data(stock_ticker, start_date, end_date):
    df = yf.download(stock_ticker, start=start_date, end=end_date)
    return df


def plot_candlestick_chart(df):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )

    fig.update_layout(
        title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price"
    )

    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
