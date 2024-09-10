
import os
import time
import pandas as pd
import ta
import ta.momentum
import ta.trend
import datetime
import argparse

import analysis.utils
# ----------------------------------------------------------------------
parser = argparse.ArgumentParser(description='stock scanner')
parser.add_argument('--date', type=str, default=datetime.datetime.today().strftime('%Y-%m-%d'), help='The date to use for processing (default: today).')

args = parser.parse_args()

date = args.date
# rsi  = args.rsi
# ----------------------------------------------------------------------
def cross_above_decl_sma(df, date):
    
    if date not in df.index:
        return False
    
    df['5_SMA']  = ta.trend.sma_indicator(close=df['Close'], window=5)

    a = df.loc[:date].iloc[-2] # yesterday
    b = df.loc[:date].iloc[-1] # today

    sma_declining = b['5_SMA'] < a['5_SMA']

    yesterday_close_below_sma = a['Close'] < a['5_SMA']
    today_close_above_sma     = b['Close'] > b['5_SMA']
    
    return sma_declining   and   yesterday_close_below_sma   and   today_close_above_sma
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)
        
    if cross_above_decl_sma(df, date):
        ls.append(pkl_file)
        print(pkl_file)
# ----------------------------------------------------------------------
elapsed_time = time.time() - start_time

print(f'Processed files: {len(pkl_files)}')

print(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------
analysis.utils.write_list_to_file(ls, output_dir='out', file=f'cross_above_decl_sma_{date}.txt')
# ----------------------------------------------------------------------
for item in ls:
    print(f'${item.replace('-1d.pkl', '')}')