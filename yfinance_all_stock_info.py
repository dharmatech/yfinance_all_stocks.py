
import os
import time
import pandas as pd
import yfinance as yf
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

# pkl_file = pkl_files[0]

start_time = time.time()
# ----------------------------------------------------------------------
ls = []

i = 0

for pkl_file in pkl_files:

    symbol = pkl_file.split('-')[0]
    # ----------------------------------------------------------------------
    elapsed_time = time.time() - start_time

    time_per_item = elapsed_time / (i+1)
    
    estimated_total_time = time_per_item * len(pkl_files)

    estimated_time_remaining = estimated_total_time - elapsed_time
    # ----------------------------------------------------------------------
    print(f'Downloading {symbol.ljust(10)} [{i+1}/{len(pkl_files)}] - Elapsed time: {elapsed_time / 60:.2f} minutes. Estimated total time: {estimated_total_time / 60 :.2f} minutes. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.')
    
    # print(f'yf.Ticker {symbol}')
    
    ticker = yf.Ticker(symbol)

    try:
        ticker_info = ticker.info

        # ticker_info['symbol'] = symbol
        
        # ls.append(ticker.info)
        ls.append(ticker_info)
    except Exception as e:
        # print(f'Error: {e}')
        # ls.append({ 'error': str(e) })
        print(f'Error getting info for {symbol}. Exception: {e}')

    i += 1

    # if i >= 10:
    #     break

df = pd.DataFrame(ls)

df.to_pickle('all_stocks_info.pkl')
# ----------------------------------------------------------------------
#
# Examples.

# load dataframe from pickle file 'all_stocks_info.pkl'

# df = pd.read_pickle('all_stocks_info.pkl')


# print(df.iloc[0].to_string())
# This doesn't print all the properties.



# for column in df.columns:
#     print(f'{column}: {df[column].iloc[0]}')
#
# This does.



# for column in sorted(df.columns):
#     print(f'{column}: {df[column].iloc[0]}')
#
# This does also, but sorted.





# print(df.iloc[0][sorted(df.columns)].to_string())

# print(df[df['symbol'] == 'AAPL'].iloc[0].to_string())

# print(df[df['symbol'] == 'AAPL'].iloc[0][sorted(df.columns)].to_string())

# print(sorted(df.columns))

# len(df.columns)

# df[df['symbol'] == 'AAPL'].iloc[0].to_csv('c:/temp/info.csv', index=True)

# df.to_csv('c:/temp/all_stocks_info.csv', index=True)


# df['symbol'].iloc[0]

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)

# 10

# df['longBusinessSummary']

# rows where 'longBusinessSummary' contains 'Apple'

# df[df['longBusinessSummary'].str.contains('Apple', na=False)]

# print(df.iloc[19].to_string())

     
# ----------------------------------------------------------------------
