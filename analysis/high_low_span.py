
import os
import time
import pandas as pd
import ta
import ta.momentum
import ta.trend
import datetime
import argparse

import analysis.utils

symbol = 'SPY'

pkl_file = f'{symbol}-1d.pkl'

file_path = os.path.join('pkl', pkl_file)

df = pd.read_pickle(file_path)

# df

# df['High'] - df['Low']

# df['High_1'] = df['High'].shift(1)

# df['Low_1'] = df['Low'].shift(1)

# df['Close_1'] = df['Close'].shift(1)



# (df['High'] - df['Low']) / df['Close'].shift(1) * 100

df['High_Low_Diff_Percent'] = (df['High'] - df['Low']) / df['Close'].shift(1) * 100

df = df.dropna(subset=['High_Low_Diff_Percent'])


# df['High_Low_Diff_Percent'].rank(pct=True) * 100

df['High_Low_Diff_Percent_Percentile'] = df['High_Low_Diff_Percent'].rank(pct=True) * 100

df






df.sort_values('High_Low_Diff_Percent').tail(10)

df.iloc[-1].name

df.sort_values('High_Low_Diff_Percent')

df_sorted = df.sort_values('High_Low_Diff_Percent')

df_sorted['Rank'] = range(1, len(df_sorted) + 1)

df_sorted['Rank'] / len(df_sorted) * 100

df_sorted['Rank_Percent'] = df_sorted['Rank'] / len(df_sorted) * 100

df_sorted

# sort by index

df_sorted.sort_index()


df_sorted.sort_index().tail(10)

