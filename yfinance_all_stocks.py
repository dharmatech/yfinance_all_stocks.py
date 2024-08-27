
import time
import yfinance_download
# ----------------------------------------------------------------------
with open('symbols.txt', 'r') as f:
    roots_stock = f.read().splitlines()
# ----------------------------------------------------------------------
start_time = time.time()

i = 0

for stock in roots_stock:

    elapsed_time = time.time() - start_time

    time_per_item = elapsed_time / (i+1)

    estimated_total_time = time_per_item * len(roots_stock)

    estimated_time_remaining = estimated_total_time - elapsed_time
    
    if '.' in stock:
        print(f'Skipping {stock.ljust(10)} [{i+1}/{len(roots_stock)}] - Elapsed time: {elapsed_time / 60:.2f} minutes. Estimated total time: {estimated_total_time / 60 / 60 :.2f} hours. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.')
    else:
        print(f'Downloading {stock.ljust(10)} [{i+1}/{len(roots_stock)}] - Elapsed time: {elapsed_time / 60:.2f} minutes. Estimated total time: {estimated_total_time / 60 / 60 :.2f} hours. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.')
        yfinance_download.update_records(symbol=stock, interval='1d')
    
    i += 1
# ----------------------------------------------------------------------
