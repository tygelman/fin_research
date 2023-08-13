import streamlit as st
import yfinance as yf
import pandas as pd


def main():
    st.title("Market Overview")

    st.write(
        "This page provides an overview of key financial information for selected stocks."
    )

    stock_tickers = st.text_area(
        "Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL"
    )
    stock_list = [ticker.strip() for ticker in stock_tickers.split(",")]

    if st.button("Show Market Overview"):
        overview_data = get_market_overview(stock_list)
        display_overview(overview_data)


def get_market_overview(stock_list):
    overview_data = []
    for ticker in stock_list:
        data = yf.Ticker(ticker)
        info = data.info
        overview_data.append(
            {
                "Ticker": ticker,
                "Company Name": info.get("longName", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "PE Ratio": info.get("trailingPE", "N/A"),
                "Dividend Yield": info.get("dividendYield", "N/A"),
                "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            }
        )
    return overview_data


def display_overview(overview_data):
    st.write("### Market Overview")
    overview_df = pd.DataFrame(overview_data)
    st.dataframe(
        overview_df.style.set_table_styles(
            [{"selector": "tr:hover", "props": [("background-color", "#e2f0ff")]}]
        ),
        width=1000,
    )


if __name__ == "__main__":
    main()
