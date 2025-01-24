
import time
import pandas as pd
import yfinance_download
# ----------------------------------------------------------------------
df = pd.read_csv('spx-constituents.csv')

start_time = time.time()
# ----------------------------------------------------------------------
ls = []

i = 0

for symbol in df['Symbol']:

    elapsed_time = time.time() - start_time

    time_per_item = elapsed_time / (i+1)
    
    estimated_total_time = time_per_item * len(df['Symbol'])
    
    estimated_time_remaining = estimated_total_time - elapsed_time
    # ----------------------------------------------------------------------
    print(f'Downloading {symbol.ljust(10)} [{i+1}/{len(df['Symbol'])}] - Elapsed time: {elapsed_time / 60:.2f} minutes. Estimated total time: {estimated_total_time / 60 :.2f} minutes. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.')
        
    yfinance_download.update_records(symbol=symbol, interval='1d')

    i += 1     
# ----------------------------------------------------------------------
