
import time
import pandas as pd
import ta
import ta.momentum
import ta.trend

import single_dataframe
# ----------------------------------------------------------------------
combined_df = single_dataframe.single_dataframe()
# ----------------------------------------------------------------------
def golden_cross_50_200(df, date):
    
    if date not in df.index:
        return False
    
    df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)
    df['50_SMA']  = ta.trend.sma_indicator(close=df['Close'], window=50)

    a = df.loc[:date].iloc[-2]
    b = df.loc[:date].iloc[-1]

    return a['50_SMA'] < a['200_SMA'] and b['50_SMA'] > b['200_SMA']
# ----------------------------------------------------------------------
date = '2024-08-27'
# ----------------------------------------------------------------------
grouped_df = combined_df.groupby('symbol')

start_time = time.time()

for symbol, df in grouped_df:

    if golden_cross_50_200(df, date):
        print(symbol)

end_time = time.time()

elapsed_time = end_time - start_time

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------