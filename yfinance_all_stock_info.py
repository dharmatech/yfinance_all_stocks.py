
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

    ls.append(ticker.info)

    i += 1

df = pd.DataFrame(ls)

df.to_pickle('all_stocks_info.pkl')
     
# ----------------------------------------------------------------------
