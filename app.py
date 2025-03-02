import pandas as pd
import streamlit as st

# Load trade results
trade_df = pd.read_csv("trade_results.csv")

st.title("Bollinger Bands Backtest Results")
st.write("This table shows all executed trades:")

st.dataframe(trade_df)

# Profit Summary
profit_summary = trade_df.groupby("token")["profit_percentage"].sum().reset_index()
st.write("Total Profit by Token:")
st.dataframe(profit_summary)

# Run with: streamlit run app.py
