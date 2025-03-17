import pandas as pd
import yfinance as yf

ticker = "MSFT"  # Change this to any ticker

# Fetch 1 year of historical data
ticker_data = yf.Ticker(ticker)
df = ticker_data.history(period="1y")

# Format column names to lowercase
df.columns = df.columns.str.lower()

# Reset index to get 'date' column
df = df.reset_index()
df = df.rename(columns={'date': 'time'})  # Rename to match lightweight_charts format

# Save the first 80% as ohlcv.csv (historical)
df.iloc[:int(len(df) * 0.8)].to_csv('ohlcv.csv', index=False)

# Save the last 20% as next_ohlcv.csv (new incoming data)
df.iloc[int(len(df) * 0.8):].to_csv('next_ohlcv.csv', index=False)

print("Saved ohlcv.csv and next_ohlcv.csv")
