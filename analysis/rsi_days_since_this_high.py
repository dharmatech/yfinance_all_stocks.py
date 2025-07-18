
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

# market_cap_min = 100

market_cap_min = args.market_cap_min if args.market_cap_min is not None else 0

# print(market_cap_min)

# if args.testing:
#     testing_count = args.testing

#     print(f'Testing mode: processing {testing_count} files only.')

# testing_count = args.testing_count if args.testing_count is not None else 100



# print(testing_count)

# exit()

# parser = argparse.ArgumentParser(description='stock scanner')
# parser.add_argument('--date', type=str, default=datetime.datetime.today().strftime('%Y-%m-%d'), help='The date to use for processing (default: today).')
# parser.add_argument('--rsi',  type=int, default=70,                                    help='The RSI threshold (default: 70).')

# args = parser.parse_args()

# date = args.date
# rsi  = args.rsi
# ----------------------------------------------------------------------

# df = pd.read_pickle(file_path)
# df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)
# df['rsi_days_since_this_high'] = -1
# ----------------------------------------------------------------------

def rsi_days_since_this_high(df):

    df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)

    df['rsi_days_since_this_high'] = -1
    
    for i in range(len(df)-1, 0, -1):
        
        if df['rsi'].iloc[i] > df['rsi'].iloc[i-1]:

            for j in range(i-1, 0, -1):

                if df['rsi'].iloc[j] >= df['rsi'].iloc[i]:
                    
                    df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = i - j

                    break

        else:
            df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = 0


# ----------------------------------------------------------------------
def rsi_days_since_this_high_last_only(df):

    df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)

    df['rsi_days_since_this_high'] = -1

    i = len(df)-1
                
    if df['rsi'].iloc[i] > df['rsi'].iloc[i-1]:

        for j in range(i-1, 0, -1):

            if df['rsi'].iloc[j] >= df['rsi'].iloc[i]:
                
                df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = i - j

                break

            if j == 0:

                df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = 1000000

    else:
        df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = 0




# ----------------------------------------------------------------------

# df.tail(50)

# i = len(df)-1
# i = i - 1

# df.loc[i-2, 'rsi_days_since_this_high']

# df.loc[i, 'rsi_days_since_this_high'] = 123

# df.iloc[i, 'rsi_days_since_this_high'] = 123

# df.iloc[i, df.columns.get_loc('rsi_days_since_this_high')] = 123





# def rsi_above(df, date, rsi=70):

#     if date not in df.index:
#         return False
    
#     df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)

#     return df.loc[date]['rsi'] > rsi

# def golden_cross_50_200(df, date):
    
#     if date not in df.index:
#         return False
    
#     df['200_SMA'] = ta.trend.sma_indicator(close=df['Close'], window=200)
#     df['50_SMA']  = ta.trend.sma_indicator(close=df['Close'], window=50)

#     a = df.loc[:date].iloc[-2]
#     b = df.loc[:date].iloc[-1]

#     return a['50_SMA'] < a['200_SMA'] and b['50_SMA'] > b['200_SMA']
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

# pkl_file = 'SPY-1d.pkl'

# ----------------------------------------------------------------------
# if len(sys.argv) > 1:
#     date = sys.argv[1]
# else:
#     date = datetime.datetime.today().strftime('%Y-%m-%d')
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

for pkl_file in pkl_files:

    print(f'Processing {pkl_file}...')
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)

    # rsi_days_since_this_high(df)
    rsi_days_since_this_high_last_only(df)

    ls.append(
        { 
            'file': pkl_file,
            'symbol': pkl_file.split('-')[0],
            'rsi_days_since_this_high': df.iloc[-1]['rsi_days_since_this_high'] 
        })

    # df.iloc[-1]['rsi_days_since_this_high']

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

# tbl.sort_values(by='rsi_days_since_this_high').tail(50)

# print(tbl.sort_values(by='rsi_days_since_this_high').tail(50))




df_info = pd.read_pickle('all_stocks_info.pkl')

tbl_b = df_info[['symbol', 'marketCap']]

# tbl

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


tbl_d = tbl_c[['symbol', 'rsi_days_since_this_high', 'market_cap_M']]

# print(tbl_d.sort_values(by='rsi_days_since_this_high').tail(50))

# market_cap_min = 200

tbl_e = tbl_d[tbl_d['market_cap_M'] >= market_cap_min]

print(tbl_e.sort_values(by='rsi_days_since_this_high').tail(50).to_string(index=False))






        
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