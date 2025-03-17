import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart

# EMA-SMA Crossover Bull Market Support Band Strategy (BMSB)

def calculate_bmsb(df):
    # Ensure the 'close' column is present and apply the ta indicators
    sma_20 = df.ta.sma(length=20)
    ema_200 = df.ta.ema(length=200)
    
    # Add the indicators to the DataFrame for easy reference
    df['SMA_20'] = sma_20
    df['EMA_200'] = ema_200
    
    # Crossover strategy: check when EMA crosses above SMA (bullish) or below (bearish)
    df['ema_sma_crossover'] = 0  # 0 = no crossover
    df.loc[df['close'] > df['SMA_20'], 'ema_sma_crossover'] = 1  # Bullish crossover
    df.loc[df['close'] < df['SMA_20'], 'ema_sma_crossover'] = -1  # Bearish crossover
    
    return sma_20, ema_200, df

if __name__ == '__main__':
    chart = Chart()
    
    ticker = "MSFT"
    ticker_data = yf.Ticker(ticker)
    df = ticker_data.history(period="4y")
    
    # Format the column names to lowercase
    df.columns = df.columns.str.lower()
    
    # Prepare indicator values for SMA and EMA using the preferred syntax
    sma_20, ema_200, df = calculate_bmsb(df)

    # Reset index to match lightweight_charts expected data format, ensure 'date' column is included
    df = df.reset_index()
    # Format the column names to lowercase
    df.columns = df.columns.str.lower()
    sma_20_df = df[['date', 'sma_20']].dropna().reset_index(drop=True)
    ema_200_df = df[['date', 'ema_200']].dropna().reset_index(drop=True)
    # Format the data for lightweight_charts
    chart.set(df)
    
    # Add SMA and EMA lines to chart
    line_sma = chart.create_line(color="green")
    
    line_sma.set(sma_20_df.rename(columns={"sma_20": "value"}))
    
    line_ema = chart.create_line(color="red")
    line_ema.set(ema_200_df.rename(columns={"ema_200": "value"}))
    
    # Add Crossover signals as dots (Bullish or Bearish)
    crossover_df = df[['date', 'ema_sma_crossover']].dropna()
    bullish_cross = crossover_df[crossover_df['ema_sma_crossover'] == 1]
    bearish_cross = crossover_df[crossover_df['ema_sma_crossover'] == -1]

    # # Add Bullish crossover dots
    # for _, row in bullish_cross.iterrows():
    #     chart.add_marker(time=row['date'], price=df.loc[df['date'] == row['date'], 'close'].values[0], color='green')
    
    # # Add Bearish crossover dots
    # for _, row in bearish_cross.iterrows():
    #     chart.add_marker(time=row['date'], price=df.loc[df['date'] == row['date'], 'close'].values[0], color='red')
    
    chart.watermark(ticker)
    chart.show(block=True)
