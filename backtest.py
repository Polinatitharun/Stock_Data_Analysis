import pandas as pd
import os

DATA_FOLDER = "data"

class BollingerBacktest:
    def __init__(self, symbol, capital_per_trade=100):
        self.symbol = symbol
        self.capital_per_trade = capital_per_trade
        self.df = self.load_data()
        self.trades = []
        self.position = 0  # Track if currently holding stock

    def load_data(self):
        """Load historical data from CSV"""
        file_path = os.path.join(DATA_FOLDER, f"{self.symbol}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
            return df
        else:
            print(f"Data file not found for {self.symbol}")
            return None

    def calculate_bollinger_bands(self, window=20, std_dev=2):
        """Calculate Bollinger Bands"""
        self.df["SMA"] = self.df["Close"].rolling(window=window).mean()
        self.df["STD"] = self.df["Close"].rolling(window=window).std()
        self.df["Upper Band"] = self.df["SMA"] + (std_dev * self.df["STD"])
        self.df["Lower Band"] = self.df["SMA"] - (std_dev * self.df["STD"])

        # Drop NaN values from early rows
        self.df.dropna(inplace=True)

    def run_backtest(self):
        """Execute trades based on Bollinger Band Reversal Strategy"""
        buy_price = None
        buy_date = None

        for index, row in self.df.iterrows():
            price = row["Close"]
            lower_band = row["Lower Band"]
            upper_band = row["Upper Band"]

            # Buy condition: Price drops below lower band
            if price < lower_band * 0.97 and buy_price is None:
                buy_price = price
                buy_date = index
                print(f"{self.symbol}: BUY at {price:.2f} on {index.date()}")

            # Sell condition: Price touches or exceeds upper band
            elif buy_price is not None and price >= upper_band:
                profit_pct = ((price - buy_price) / buy_price) * 100
                self.trades.append([self.symbol, buy_date, buy_price, index, price, profit_pct])
                print(f"{self.symbol}: SELL at {price:.2f} on {index.date()} | Profit: {profit_pct:.2f}%")
                buy_price = None  # Reset

        # Sell remaining holdings at end
        if buy_price is not None:
            final_price = self.df.iloc[-1]["Close"]
            profit_pct = ((final_price - buy_price) / buy_price) * 100
            self.trades.append([self.symbol, buy_date, buy_price, self.df.index[-1], final_price, profit_pct])
            print(f"{self.symbol}: FINAL SELL at {final_price:.2f} on {self.df.index[-1].date()} | Profit: {profit_pct:.2f}%")

    def get_trade_history(self):
        """Return trade history as DataFrame"""
        return pd.DataFrame(self.trades, columns=["token", "date_in", "buy_price", "date_out", "sell_price", "profit_percentage"])

# Run backtest for all stocks
SYMBOLS = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "BTC-USD", "ETH-USD"]  # Add 50 symbols
all_trades = []

for symbol in SYMBOLS:
    backtest = BollingerBacktest(symbol)
    if backtest.df is not None:
        backtest.calculate_bollinger_bands()
        backtest.run_backtest()
        all_trades.append(backtest.get_trade_history())

# Save all trade history
final_trades_df = pd.concat(all_trades, ignore_index=True)
final_trades_df.to_csv("trade_results.csv", index=False)
print("Trade history saved to trade_results.csv")
