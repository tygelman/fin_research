import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Moving Average Buy/Sell Signals")

stock_name = st.text_input("Enter a ticker")
start_date = st.date_input("Enter a start date")
end_date = st.date_input("Enter an end date")

cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
graph_cols = st.multiselect("Select columns to graph", cols)

moving_average_data = []
for idx in range(2):  # Limit to two moving averages
    ma_column = st.selectbox(
        f"Select a column for Moving Average {idx+1}", cols, key=f"ma_column_{idx}"
    )
    ma_days = st.number_input(
        f"Enter number of days for Moving Average {idx+1}",
        min_value=1,
        value=10,
        key=f"ma_days_{idx}",
    )
    moving_average_data.append((ma_column, ma_days))

if st.button("Load Data and Display"):
    # Convert date objects to strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Download data
    df = yf.download(stock_name, start=start_date_str, end=end_date_str)

    st.write(f"### Full Data:")
    st.dataframe(df, width=1000)  # Display all columns

    if len(graph_cols) > 0:
        st.write(f"### Line Chart:")

        # Create a new DataFrame for plotting
        plot_df = df[graph_cols].copy()

        # Calculate and add moving averages to the DataFrame
        for ma_column, ma_days in moving_average_data:
            if ma_column in graph_cols:
                moving_avg = df[ma_column].rolling(window=ma_days).mean()
                moving_avg_label = f"{ma_column} Moving Avg ({ma_days} days)"
                plot_df[moving_avg_label] = moving_avg

        # Plot the selected columns and their respective moving averages on the same chart
        st.line_chart(plot_df, use_container_width=True)
