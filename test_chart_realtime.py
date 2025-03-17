import pandas as pd
from numpy import nan as npNaN
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart
from time import sleep

if __name__ == '__main__':
    
    chart = Chart()
    ticker = 'BTC-USD'
    msft = yf.Ticker(ticker)
    df = msft.history(period="4y")

    df = df.reset_index()
    df.columns = df.columns.str.lower()
    df = df.rename(columns={'date': 'time'})  # Rename to match lightweight_charts format

    # Save the first 20% as ohlcv (historical)
    df1 = df.iloc[:int(len(df) * 0.2)]

    # Save the last 80% as next_ohlcv (new incoming data)
    df2 = df.iloc[int(len(df) * 0.2):]

    # print(df_ohlcv.head())
    # print(df_next_ohlcv.head())

    chart.set(df1)

    chart.watermark(ticker)

    chart.show()

    last_close = df1.iloc[-1]['close']
    
    for i, series in df2.iterrows():
        chart.update(series)

        if series['close'] > 60000 and last_close < 60000:
            chart.marker(text='The price crossed $60000!')
            
        last_close = series['close']
        sleep(0.1)