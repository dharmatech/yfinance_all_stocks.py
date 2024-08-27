
import sys
import os
import time
import pandas as pd
import ta
import ta.momentum
import ta.trend
import datetime

import analysis.utils
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
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
if len(sys.argv) > 1:
    date = sys.argv[1]
else:
    date = datetime.today().strftime('%Y-%m-%d')
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)
        
    if golden_cross_50_200(df, date):
        ls.append(pkl_file)
        print(pkl_file)
# ----------------------------------------------------------------------
elapsed_time = time.time() - start_time

print(f'Processed files: {len(pkl_files)}')

print(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------
analysis.utils.write_list_to_file(ls, output_dir='out', file=f'cross_above_200_day_sma_{date}.txt')