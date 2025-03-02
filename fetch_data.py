import yfinance as yf
import pandas as pd
import os

# List of 50 stocks/crypto to fetch data for
SYMBOLS = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "BTC-USD", "ETH-USD"]  # Add 50 symbols

# Create folder for data storage
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def fetch_stock_data(symbol, period="1y", interval="1d"):
    """Fetch historical stock/crypto data and save as CSV"""
    stock = yf.Ticker(symbol)
    df = stock.history(period=period, interval=interval)

    if not df.empty:
        file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")
        df.to_csv(file_path)
        print(f"Data saved: {file_path}")
    else:
        print(f"Failed to fetch data for {symbol}")

# Fetch data for all symbols
for symbol in SYMBOLS:
    fetch_stock_data(symbol)
