import streamlit as st
import yfinance as yf
import pandas as pd


def main():
    st.title("Stock Comparison")

    stock_tickers = st.text_area("Enter stock tickers (comma-separated)", "AAPL, MSFT")
    stock_list = [ticker.strip().upper() for ticker in stock_tickers.split(",")]

    start_date = st.date_input("Enter a start date")
    end_date = st.date_input("Enter an end date")

    if st.button("Compare Stocks"):
        data = download_data(stock_list, start_date, end_date)
        plot_comparison(data)


def download_data(stock_list, start_date, end_date):
    data = {}
    for stock in stock_list:
        df = yf.download(stock, start=start_date, end=end_date)
        data[stock] = df["Adj Close"]
    return pd.DataFrame(data)


def plot_comparison(data):
    st.write("### Stock Price Comparison")
    st.line_chart(data, use_container_width=True)


if __name__ == "__main__":
    main()
