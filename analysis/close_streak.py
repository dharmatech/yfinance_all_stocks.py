
import sys
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
parser = argparse.ArgumentParser()

parser.add_argument('--market_cap_min', type=int, default=0, help='Minimum market cap in millions (default: 0).')
parser.add_argument('--testing_count', type=int)

args = parser.parse_args()

# args.testing_count = 100

# market_cap_min = 100

market_cap_min = args.market_cap_min if args.market_cap_min is not None else 0
# ----------------------------------------------------------------------

def calculate_close_streak_column(df):

    tmp = df.copy()[['Close']]
    
    tmp['Close_1'] = tmp['Close'].shift(1)

    tmp['diff'] = tmp['Close'] - tmp['Close_1']

    tmp.loc[tmp['diff'] > 0, 'sign'] = 'pos'
    tmp.loc[tmp['diff'] < 0, 'sign'] = 'neg'
    tmp.loc[tmp['diff'] == 0, 'sign'] = 'zero'

    tmp['new_streak'] = tmp['sign'] != tmp['sign'].shift()

    tmp['streak_id'] = tmp['new_streak'].cumsum()

    tmp['streak_count'] = tmp.groupby('streak_id').cumcount() + 1

    tmp.tail(30)

    return tmp
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

# pkl_file = 'SPY-1d.pkl'
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

# pkl_file = 'SVA-1d.pkl'

for pkl_file in pkl_files:

    print(f'Processing {pkl_file}...')
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)

    # rsi_days_since_this_high(df)
    # rsi_days_since_this_high_last_only(df)

    tmp = calculate_close_streak_column(df)

    ls.append(
        { 
            'file': pkl_file,
            'symbol': pkl_file.split('-')[0],
            # 'rsi_days_since_this_high': df.iloc[-1]['rsi_days_since_this_high'] 
            'close_streak_count': tmp['streak_count'].iloc[-1],
            'close_streak_sign':  tmp['sign'].iloc[-1],
        })

    # For testing. Only process a few files.
    # 
    # if len(ls) > 1000:
    #     break

    if args.testing_count is not None:
        if len(ls) >= args.testing_count:
            print(f'Testing mode: processed {len(ls)} files. Exiting.')
            break
    

# create a dataframe from `ls`

tbl = pd.DataFrame(ls)

# Table for stock info.

df_info = pd.read_pickle('all_stocks_info.pkl')

tbl_b = df_info[['symbol', 'marketCap']]


# tbl = pd.merge(tbl, tbl_b, on='symbol', how='left')

tbl_c = pd.merge(left=tbl, right=tbl_b, how='left', on='symbol')


# tbl_c['marketCap'].astype('Int64')  # Use 'Int64' to allow for NaN values

# tbl_c['market_cap'] = tbl_c['marketCap'].astype('Int64')


# tbl_c['market_cap_M'] = tbl_c['marketCap'] / 1000000

# tbl_c['market_cap_M'] = tbl_c['marketCap'].astype('Int64')

tbl_c['market_cap_M'] = (tbl_c['marketCap'].astype('Int64') / 1000000).astype('Int64')


# (tbl_c['marketCap'] / 1000000).astype('Int64')

# tbl_c

# pkl_files[0].split('-')[0]


# tbl_d = tbl_c[['symbol', 'rsi_days_since_this_high', 'market_cap_M']]

tbl_d = tbl_c.drop(columns=['file', 'marketCap'])



# print(tbl_d.sort_values(by='rsi_days_since_this_high').tail(50))

# market_cap_min = 200

tbl_e = tbl_d[tbl_d['market_cap_M'] >= market_cap_min]

tbl_f = tbl_e.sort_values(by='close_streak_count')

tbl_g = tbl_f[tbl_f['close_streak_sign'] != 'zero']

# print(tbl_e.sort_values(by='rsi_days_since_this_high').tail(50).to_string(index=False))

print(tbl_g.sort_values(by='close_streak_count').tail(50).to_string(index=False))






        
    # if rsi_above(df, date, rsi=rsi):
    #     ls.append(pkl_file)
    #     print(pkl_file)
# ----------------------------------------------------------------------
elapsed_time = time.time() - start_time

print(f'Processed files: {len(pkl_files)}')

print(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------
# analysis.utils.write_list_to_file(ls, output_dir='out', file=f'rsi_above_{date}.txt')
# ----------------------------------------------------------------------
# for item in ls:
#     print(f'${item.replace('-1d.pkl', '')}')