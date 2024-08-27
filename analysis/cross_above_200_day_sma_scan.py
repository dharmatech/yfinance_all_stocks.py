
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

    a = df.loc[:date].iloc[-2]
    b = df.loc[:date].iloc[-1]

    return a['Close'] < a['200_SMA'] and b['Close'] > b['200_SMA']
# ----------------------------------------------------------------------
if len(sys.argv) > 1:
    date = sys.argv[1]
else:
    date = datetime.today().strftime('%Y-%m-%d')
# ----------------------------------------------------------------------
def proc(df):
    df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)

def pred(df, date):
    return cross_above_200_day_sma(df, date)

pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

ls = utils.scan(pkl_files, date, proc, pred)
# ----------------------------------------------------------------------
pprint.pprint(ls)

pprint.pprint(f'Processed files: {len(pkl_files)}')

pprint.pprint(f'Items found: {len(ls)}')
# ----------------------------------------------------------------------
utils.write_list_to_file(ls, output_dir='out', file=f'cross_above_200_day_sma_{date}.txt')