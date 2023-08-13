import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def main():
    st.title("Historical Price Lookup")

    stock_ticker = st.text_input("Enter a stock ticker", "AAPL")
    start_date = st.date_input("Enter a start date")
    end_date = st.date_input("Enter an end date")

    if st.button("Show Historical Prices"):
        df = download_data(stock_ticker, start_date, end_date)
        plot_prices(df)


def download_data(stock_ticker, start_date, end_date):
    df = yf.download(stock_ticker, start=start_date, end=end_date)
    return df


def plot_prices(df):
    st.write("### Historical Prices")
    st.line_chart(df["Close"], use_container_width=True)


if __name__ == "__main__":
    main()
