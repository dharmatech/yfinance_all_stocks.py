
import sys
import os
import time
import pandas as pd
import pprint
import ta
import ta.momentum
import ta.trend
import datetime

import utils
# ----------------------------------------------------------------------
def cross_above_200_day_sma(df, date):
    
    if date not in df.index:
        return False

    # a = df.loc[:date].iloc[-2]
    # b = df.loc[date]

    a = df.loc[:date].iloc[-2]
    b = df.loc[:date].iloc[-1]

    return a['Close'] < a['200_SMA'] and b['Close'] > b['200_SMA']
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
if len(sys.argv) > 1:
    date = sys.argv[1]
else:
    date = datetime.today().strftime('%Y-%m-%d')
# ----------------------------------------------------------------------
start_time = time.time()

ls = []

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)

    df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)
    
    if cross_above_200_day_sma(df, date):
        ls.append(pkl_file)
        print(f'{pkl_file.ljust(20)} - {df.loc[date]["200_SMA"]}')

elapsed_time = time.time() - start_time

pprint.pprint(ls)

pprint.pprint(f'Processed files: {len(pkl_files)}')

pprint.pprint(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------

def analyze_files(pkl_files, date, proc, pred):
    ls = []

    for pkl_file in pkl_files:
        
        file_path = os.path.join('pkl', pkl_file)

        df = pd.read_pickle(file_path)

        # df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)

        proc(df)
        
        # if cross_above_200_day_sma(df, date):
        #     ls.append(pkl_file)
        #     print(f'{pkl_file.ljust(20)} - {df.loc[date]["200_SMA"]}')

        if pred(df, date):
            ls.append(pkl_file)
            print(f'{pkl_file.ljust(20)} - {df.loc[date]["200_SMA"]}')

    return ls

def proc(df):
    df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)

def pred(df, date):
    return cross_above_200_day_sma(df, date)

ls = analyze_files(pkl_files, date, proc, pred)

# ----------------------------------------------------------------------
utils.write_list_to_file(ls, output_dir='out', file=f'cross_above_200_day_sma_{date}.txt')