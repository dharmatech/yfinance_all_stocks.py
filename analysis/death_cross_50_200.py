
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
def death_cross(df, date, x=50, y=200):
    
    if date not in df.index:
        return False
    
    df[f'{y}_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=y)
    df[f'{x}_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=x)

    a = df.loc[:date].iloc[-2]
    b = df.loc[:date].iloc[-1]

    return a[f'{x}_SMA'] > a[f'{y}_SMA'] and b[f'{x}_SMA'] < b[f'{y}_SMA']
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
        
    if death_cross(df, date, x=50, y=200):
        ls.append(pkl_file)
        print(pkl_file)
# ----------------------------------------------------------------------
elapsed_time = time.time() - start_time

print(f'Processed files: {len(pkl_files)}')

print(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------
analysis.utils.write_list_to_file(ls, output_dir='out', file=f'death_cross_50_200_{date}.txt')
# ----------------------------------------------------------------------

for item in ls:
    item = item.replace('-1d.pkl', '')
    item = f'${item}'
    print(item)