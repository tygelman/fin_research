import streamlit as st
import yfinance as yf
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob


def main():
    st.title("News and Sentiment Analysis")

    stock_ticker = st.text_input("Enter a stock ticker", "AAPL")
    start_date = st.date_input("Enter a start date (As of July 11, 2023)")
    end_date = st.date_input("Enter an end date")

    if st.button("Fetch News and Analyze Sentiment"):
        news_df = fetch_news(stock_ticker, start_date, end_date)
        sentiment_df = analyze_sentiment(news_df)
        display_results(news_df, sentiment_df)


def fetch_news(stock_ticker, start_date, end_date):
    newsapi = NewsApiClient(api_key="eaf289d0507b44b5aef39229f4af36e4")
    response = newsapi.get_everything(
        q=stock_ticker,
        from_param=start_date,
        to=end_date,
        language="en",
        sort_by="publishedAt",
    )
    articles = response.get("articles", [])

    news_data = []
    for article in articles:
        news_data.append(
            {
                "Date": article["publishedAt"],
                "Source": article["source"]["name"],
                "Title": article["title"],
                "Description": article["description"],
                "URL": article["url"],
            }
        )

    news_df = pd.DataFrame(news_data)
    return news_df


def analyze_sentiment(news_df):
    sentiment_scores = []

    for description in news_df.get("Description", []):
        analysis = TextBlob(description)
        sentiment_scores.append(analysis.sentiment.polarity)

    news_df["Sentiment"] = sentiment_scores
    return news_df


def display_results(news_df, sentiment_df):
    st.write("### News Headlines and Sentiment Analysis")

    if not news_df.empty:
        st.dataframe(news_df, width=800)

        st.write("### Sentiment Analysis")
        st.line_chart(sentiment_df.set_index("Date")["Sentiment"])

    else:
        st.write("No news headlines found for the selected period.")


if __name__ == "__main__":
    main()
