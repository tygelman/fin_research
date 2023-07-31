import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.sidebar.markdown("# Position Query")

st.title('Security Positions')

security = st.text_input('Enter security (e.g. META__230721C00230000) or name (e.g. META) for all positions')

all_account_names = [""]

selected_accounts = st.multiselect('Select accounts', options=all_account_names, default="All Accounts")

start_date = st.date_input('Select start date')
end_date = st.date_input('Select end date', value=datetime.today())

start_date_str = start_date.strftime('%Y%m%d')
end_date_str = end_date.strftime('%Y%m%d')

if start_date_str and end_date_str:
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.strptime(end_date_str, '%Y%m%d')

    num_days = (end_date - start_date).days

    all_dates = []
    for i in range(num_days + 1):
        current_date = start_date + timedelta(days=i)
        all_dates.append(current_date.strftime('%Y%m%d'))

    button_clicked = st.button('Load Data')

    if button_clicked:
        dfs = []
        for date in all_dates:
            try:
                df = pd.read_csv(f'/.csv')
                df['date'] = pd.to_datetime(date, format='%Y%m%d') 
                filtered_df = df[df['symbol'].str.startswith(security)]
                filtered_df['date'] = filtered_df['date'].astype(str).str.split(' ').str[0]
                
                if "All Accounts" not in selected_accounts:
                    filtered_df = filtered_df[filtered_df['account'].isin(selected_accounts)]
                filtered_df.drop(columns=['account'], inplace=True)  
                dfs.append(filtered_df)
            
            except FileNotFoundError:
                st.write(f'{date} is a weekend or holiday; file for {date} does not exist.')

        if dfs:  
            concatenated_df = pd.concat(dfs)
            st.dataframe(concatenated_df, width=10000, height=800)

            options = list(concatenated_df['symbol'].unique())
            selected_security = st.selectbox('Select a security for the plot', options)

            plot_button_clicked = st.button('Show Plot')
            if plot_button_clicked:
                df_for_plot = concatenated_df[concatenated_df['symbol'] == selected_security]

                fig = px.line(df_for_plot, x='date', y='pos', title=f'Position over time for {selected_security}')
                fig.update_layout(autosize=False, width=800, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=4))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data found for the given dates and security.')
